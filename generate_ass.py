import json

def generate_ass(font, data):
    segments = data.get("segments", [])

    # Format seconds to ASS time (h:mm:ss.cc)
    def format_time(sec):
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = int(sec % 60)
        cs = int(round((sec - int(sec)) * 100))
        # Handle rounding edge cases (59.998s -> 1:00.00)
        if cs == 100:
            s += 1
            cs = 0
            if s == 60:
                m += 1
                s = 0
                if m == 60:
                    h += 1
                    m = 0
        return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

    def group_words(words, max_words=4):
        phrases = []
        current = []
        for i, w in enumerate(words):
            text = w["word"]
            if not text or text.isspace():
                continue
            current.append(w)
            end_char = text.strip()[-1] if text.strip() else ""
            # Decide if we should break the phrase here
            if end_char in ".?!":
                phrases.append(current)
                current = []
            elif end_char in ",;:" and len(current) >= 3:
                # break at comma/semicolon if phrase is at least 3 words
                phrases.append(current)
                current = []
            elif len(current) >= max_words and i < len(words) - 1:
                # If we've hit ~4 words and next word isn't punctuation-ended, break here
                next_word = words[i+1]["word"].strip() if words[i+1]["word"] else ""
                next_end = next_word[-1] if next_word else ""
                if next_end not in ".?!,":
                    phrases.append(current)
                    current = []
                # else: if next word *does* end in punctuation, we wait to break at the punctuation
        if current:
            phrases.append(current)
        return phrases

    ass_lines = []

    # Script Info section
    ass_lines.append("[Script Info]")
    ass_lines.append("ScriptType: v4.00+")
    ass_lines.append("PlayResX: 1080")
    ass_lines.append("PlayResY: 1920")
    ass_lines.append("WrapStyle: 0")
    ass_lines.append("ScaledBorderAndShadow: yes")
    ass_lines.append(""); ass_lines.append("");

    # Styles section
    ass_lines.append("[V4+ Styles]")
    ass_lines.append("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
                    "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
                    "Alignment, MarginL, MarginR, MarginV, Encoding")
    # Define the default style: Montserrat 64px, white text, bold, with black outline, bottom-center
    fontname = "Montserrat" if font.lower() == "montserrat" else "Roboto"
    # Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, 
    #     Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, 
    #     BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
    style = f"Style: Default,{fontname},70,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,2,0,2,200,200,150,1"
    ass_lines.append(style)
    ass_lines.append(""); ass_lines.append("");

    # Events section
    ass_lines.append("[Events]")
    ass_lines.append("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text")

    # Define colors and scale for convenience (BGR hex format in ASS, with &H prefix and & suffix)
    highlight_color = "&H00FFFF&"   # Yellow (00BBGGRR: 00 (blue) FF (green) FF (red) => #FFFF00)
    default_color   = "&H00FFFFFF&" # White
    highlight_scale = 103  # 103% scale
    default_scale   = 100  # 100% scale

    for seg in segments:
        phrase_list = group_words(seg.get("words", []))
        for phrase in phrase_list:
            if not phrase: 
                continue
            start_time = format_time(phrase[0]["start"])
            end_time   = format_time(phrase[-1]["end"])
            # Build the dialogue text with override tags for each word
            parts = []
            phrase_start_sec = phrase[0]["start"]
            for idx, word_info in enumerate(phrase):
                word = word_info["word"].strip()
                if word == "":
                    continue
                word_text = word.upper()  # uppercase text
                # Calculate word's start and end times relative to the phrase start (in milliseconds)
                rel_start = int(round((word_info["start"] - phrase_start_sec) * 1000))
                rel_end   = int(round((word_info["end"] - phrase_start_sec) * 1000))
                if rel_end < rel_start:
                    rel_end = rel_start  # safety
                # Construct override tag for this word
                if idx == 0:
                    # First word: start highlighted immediately, then revert at end
                    part = (f"{{\\1c{highlight_color}\\fscx{highlight_scale}\\fscy{highlight_scale}"
                            f"\\t({rel_end},{rel_end},\\1c{default_color}\\fscx{default_scale}\\fscy{default_scale})}}"
                            f"{word_text}")
                else:
                    # Other words: start in default style, highlight at word start, revert at word end
                    part = (f"{{\\1c{default_color}\\fscx{default_scale}\\fscy{default_scale}"
                            f"\\t({rel_start},{rel_start},\\1c{highlight_color}\\fscx{highlight_scale}\\fscy{highlight_scale})"
                            f"\\t({rel_end},{rel_end},\\1c{default_color}\\fscx{default_scale}\\fscy{default_scale})}}"
                            f"{word_text}")
                parts.append(part)
            # Join the parts with a space (space outside of override braces so it retains default styling)
            dialogue_text = " ".join(parts)
            ass_lines.append(f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{dialogue_text}")

    # Write the ASS content to a file
    with open("output.ass", "w", encoding="utf-8") as out:
        out.write("\n".join(ass_lines))
    
    print("ASS File Generation Finished")
