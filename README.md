🎬 AI-Powered Subtitle Generator

This Python tool transcribes a video using Faster-Whisper, generates animated karaoke-style subtitles in ASS format, and burns them into the video using ffmpeg.
🧰 Features

    Transcription using Whisper (tiny to large-v2)

    Word-by-word animated subtitles (ASS format)

    Stylish subtitle overlay using either Montserrat or Roboto

    Embedded font support via fontsdir in ffmpeg

🚀 How to Use
1. Install Requirements

pip install -r requirements.txt

You also need:

    FFmpeg with libass support

    Fonts placed in ./fonts/Montserrat/static/ and ./fonts/Roboto/static/

2. Run the Script

python subtitle.py <path_to_video> [--model MODEL] [--font FONT] [--output OUTPUT]

🔧 Arguments
Argument	Description
video	Path to input video file
--model	Whisper model to use (tiny, base, small, medium, large-v2)
--font	Subtitle font: montserrat (default) or roboto
--output	Path to output video with burned-in subtitles (default: output_subbed.mp4)