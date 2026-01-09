import subprocess
import json
from pathlib import Path

def probe_video(video_path: str) -> dict:
    """
    Uses ffprobe to extract metadata from a video file.
    """
    cmd = [
        "ffprobe",
        "-v", "error",
        "-print_format", "json",
        "-show_streams",
        "-show_format",
        video_path
    ]

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {result.stderr}")

    data = json.loads(result.stdout)

    video_stream = next(
        s for s in data["streams"] if s["codec_type"] == "video"
    )

    fps = eval(video_stream.get("avg_frame_rate", "0"))
    width = video_stream.get("width")
    height = video_stream.get("height")
    duration = float(data["format"].get("duration", 0))

    return {
        "fps": fps,
        "width": width,
        "height": height,
        "duration": duration,
        "codec": video_stream.get("codec_name"),
    }
