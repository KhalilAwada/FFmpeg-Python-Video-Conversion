import os
import fnmatch
import subprocess
import re  # Add this line to import the 're' module
from tqdm import tqdm
from ffmpeg_progress_yield import FfmpegProgress

import sys
from decimal import *

def find_video_files(directory):
    video_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if fnmatch.fnmatch(file.lower(), '*.mov') or fnmatch.fnmatch(file.lower(), '*.mp4'):
                video_files.append(os.path.join(root, file))
    
    return video_files



def read_converted_files(file_path):
    try:
        with open(file_path, 'r') as file:
            return set(file.read().splitlines())
    except FileNotFoundError:
        return set()

def write_converted_file(file_path, converted_files):
    with open(file_path, 'a') as file:
        for converted_file in converted_files:
            file.write(f"{converted_file}\n")

# def convert_to_mp4(input_file, output_file):
#     ffmpeg_command = [
#         'ffmpeg',
#         '-i', input_file,
#         '-c:v', 'libx264',
#         '-c:a', 'aac',
#         '-strict', 'experimental',
#         output_file
#     ]

#     process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

#     for line in process.stderr:
#         print(line.strip())

#     process.wait()

#     if process.returncode == 0:
#         print("Conversion completed successfully.")
#     else:
#         print(f"Conversion failed with return code {process.returncode}.")


def convert_to_mp4(input_file, output_file):
    ffmpeg_command = [
        'ffmpeg',
        '-i', input_file,
        '-vf', 'scale=1280:720',
        '-r', '30',
        '-c:a', 'copy',
        '-map_metadata', '0',
        output_file
    ]

    process = subprocess.Popen(ffmpeg_command, stderr=subprocess.PIPE, text=True)

    with tqdm(total=100, unit='%', unit_scale=True, desc='Conversion Progress') as pbar:
        for line in process.stderr:
            pbar.update(1)
    
    process.wait()

    if process.returncode == 0:
        print("Conversion completed successfully.")
    else:
        print(f"Conversion failed with return code {process.returncode}.")


def main():
    # directory_to_search = input("Enter the directory path to search: ")
    directory_to_search = sys.argv[-1]

    converted_files_file = "/mnt/converted_files.txt"

    if not os.path.exists(directory_to_search):
        print("Invalid directory path. Please provide a valid path.")
        return

    video_files = find_video_files(directory_to_search)

    if not video_files:
        print("No .mov or .mp4 files found in the specified directory and its subdirectories.")
    else:
        print("Found the following video files:")

        for video_file in video_files:
            converted_files = read_converted_files(converted_files_file)
            if video_file not in converted_files:

                print(video_file)
            
                # Define the output file path with .mp4 extension
                output_file = os.path.splitext(video_file)[0] + '_.mp4'
                
                # Convert the video file to .mp4 using FFmpeg with progress
                if convert_to_mp4(video_file, output_file):
                    converted_files.add(video_file)
                    write_converted_file(converted_files_file, {video_file})
            else:
                print("already converted skipping :")
                print(video_file)

if __name__ == "__main__":
    main()
