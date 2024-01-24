import os
import fnmatch
import subprocess
import re  # Add this line to import the 're' module
# from tqdm import tqdm
# from ffmpeg_progress_yield import FfmpegProgress
from ffmpeg_progress import start
import subprocess as sp
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

def convert_to_mp4(infile, outfile, vstats_path):
    try:
        start(infile, outfile, ffmpeg_callback, on_message=on_message_handler, on_done=lambda: sys.stdout.write(' \r'+infile+ ' Converted'), wait_time=1)
        return True
    except Exception as e:
        print(f"Error during conversion: {e}")
        return False

def progress(percent=0, width=40):
    left = width * percent // 100
    right = width - left
    
    tags = "#" * left
    spaces = " " * right
    percents = f"{percent:.0f}%"
    print("\r [", tags, spaces, "] ", percents, sep="", end="", flush=True)

    return "["+ tags+ spaces+ "]"

def ffmpeg_callback(infile: str, outfile: str, vstats_path: str):
    return sp.Popen(['ffmpeg',
                     '-nostats',
                     '-loglevel', '0',
                     '-y',
                     '-vstats_file', vstats_path,
                     '-i', infile,
                     '-vf', 'scale=1280:720',
                     '-r', '30',
                     '-c:a', 'copy',
                     '-map_metadata', '0',
                      outfile]).pid

def on_message_handler(percent: float,
                       fr_cnt: int,
                       total_frames: int,
                       elapsed: float):
    
    integer= round(Decimal('{:.2f}'.format(percent)))
    sys.stdout.write(' \r{:.2f}%'.format(percent)+' '+str(progress(integer)))
    # print()
    # print(str(progress(integer)), ' \r{:.2f}%'.format(percent), flush=True)
    sys.stdout.flush()

def main():
    # directory_to_search = input("Enter the directory path to search: ")
    directory_to_search = sys.argv[-1]

    converted_files_file = "/mnt/nfs/converted_files.txt"

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
                output_file = os.path.splitext(video_file)[0] + '_'+ os.path.splitext(video_file)[1]
                
                # Convert the video file to .mp4 using FFmpeg with progress
                if convert_to_mp4(video_file, output_file, '/app/vstats_file.txt'):
                    converted_files.add(video_file)
                    write_converted_file(converted_files_file, {video_file})
                    os.remove(video_file)
                    os.rename(output_file, video_file)
                else:
                    print("could not convert: "+str(video_file))

            else:
                print("already converted skipping :")
                print(video_file)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nConversion interrupted by user.")
