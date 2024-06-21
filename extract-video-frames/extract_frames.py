"""
Project: Video Frame Extraction
Author: Brian Ebiyau
Date: 6/21/2024
Description: This script extracts frames from videos at a specified rate and saves them to an output directory.
             It can process multiple videos from a specified input folder.

Requirements:
- cv2 (OpenCV)
- os

Usage:
- Ensure that the required packages are installed.
- Place the input videos in the specified input folder.
- Set the parameters (input_folder, output_folder, frame_rate).
- Run the script to extract frames from each video in the input folder.
"""

import cv2
import os

def create_output_directory(output_directory):
    """
    Create the output directory if it does not exist.

    Args:
        output_directory (str): Path to the directory where extracted frames will be saved.
    """
    if not os.path.exists(output_directory):
        print(f'Created output directory {output_directory}...')
        os.makedirs(output_directory)
    else:
        print(f'Directory already exists {output_directory}...')

def extract_frames_from_video(video_path, output_directory, frame_rate=1):
    """
    Extract frames from a video at a consistent rate.

    Args:
        video_path (str): Path to the input video file.
        output_directory (str): Directory where extracted frames will be saved.
        frame_rate (int): Number of frames to extract per second.
    """
    # Create the output directory
    create_output_directory(output_directory=output_directory)
    
    # Capture the video
    cap = cv2.VideoCapture(video_path)
    
    # Get the original frame rate of the video
    original_frame_rate = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(original_frame_rate / frame_rate)
    
    frame_count = 0
    extracted_frame_count = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Save frame if it is at the specified interval
        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_directory, f"frame_{extracted_frame_count:05d}.jpg")
            cv2.imwrite(frame_filename, frame)
            extracted_frame_count += 1
            
        frame_count += 1
    
    cap.release()

def process_video_in_folder(input_folder, output_directory, frame_rate):
    """
    Process all videos in the input folder and extract frames.

    Args:
        input_folder (str): Folder containing the input video files.
        output_directory (str): Directory where extracted frames will be saved.
        frame_rate (int): Number of frames to extract per second.
    """
    for video_filename in os.listdir(input_folder):
        if video_filename.endswith(('.mp4', '.avi', '.mov', '.mkv')):
            video_path = os.path.join(input_folder, video_filename)
            video_output_folder = os.path.join(output_directory, os.path.splitext(video_filename)[0])
            extract_frames_from_video(video_path, video_output_folder, frame_rate)

# Set parameters
input_folder = 'kabisa-videos'
output_folder = 'extracted_frames'
frame_rate = 1

# Process the videos
process_video_in_folder(input_folder, output_folder, frame_rate)
