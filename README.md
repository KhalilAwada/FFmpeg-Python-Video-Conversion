# Video Conversion Script with FFmpeg

This Python script utilizes FFmpeg to recursively search for `.mov` and `.mp4` files in a specified directory and its subdirectories. It converts these video files to the `.mp4` format with progress tracking, deletes the original file upon successful conversion, and renames the new file to the original name.

## Requirements

- Python 3
- FFmpeg
- [ffmpeg_progress](https://pypi.org/project/ffmpeg-progress/)

## Installation

1. Clone the repository or download the script.
2. Install the required Python packages:

   ```bash
   pip install ffmpeg-progress

## Usage
```python script_name.py /path/to/directory```
 or 
```docker run -it --rm -e PYTHONUNBUFFERED=1 -v /mnt/nfs:/mnt/nfs -v $(pwd)/app:/app --entrypoint "" ffmpeg-python:latest python -u app.py /mnt/nfs/GoPro/```
