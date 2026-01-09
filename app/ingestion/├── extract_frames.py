import subprocess
from pathlib import Path

def extract_frames(
    video_path: str,
    output_dir: str,
    fps: int = 5
):
    """
    Extract frames at fixed FPS for analysis.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"fps={fps}",
        f"{output_dir}/frame_%06d.jpg"
    ]

    subprocess.run(cmd, check=True)
