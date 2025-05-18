import argparse
import subprocess
from pathlib import Path
from transcribe import transcribe
from generate_ass import generate_ass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("video", help="Path to video file")
    parser.add_argument("--model", default="large-v2", help="Model size (e.g., tiny, base, small, medium, large-v2)")
    parser.add_argument("--font", default="montserrat", choices=["montserrat", "roboto"], help="Font to use for subtitles")
    parser.add_argument("--output", default="output_subbed.mp4", help="Path to subtitled output file")
    args = parser.parse_args()

    generate_ass(args.font, transcribe(args.video, args.model))

    fonts_dir = Path(__file__).resolve().parent / "fonts"
    if args.font == "montserat":
        fonts_dir = fonts_dir / "Montserrat" / "static"
    else:
        fonts_dir = fonts_dir / "Roboto" / "static"

    cmd = [
        "ffmpeg",
        "-i", args.video,
        "-vf", f"subtitles=output.ass:fontsdir={fonts_dir}",
        "-c:a", "copy",
        args.output
    ]
    subprocess.run(cmd, check=True)

if __name__ == '__main__':
    main()

 