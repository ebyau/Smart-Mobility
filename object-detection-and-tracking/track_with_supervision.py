"""
Project: Object Detection and Tracking with YOLOv8 and Supervision
Author: Brian Ebiyau
Date: 6/21/2024
Description: This script utilizes the YOLOv8 model for object detection and ByteTrack for object tracking.
             It processes a video, detects objects of a specific class (motorcycles), annotates bounding boxes
             and labels, and saves the annotated video.

Credit: This script is based on the example provided by Supervision at:
        https://supervision.roboflow.com/latest/how_to/track_objects/

Requirements:
- numpy
- supervision
- ultralytics

Usage:
- Ensure that the required packages are installed.
- Place the input video file in the same directory as this script or update the source_path variable.
- Run the script to process the video and generate an annotated output video.
"""

import numpy as np
import supervision as sv
from ultralytics import YOLO

# Initialize YOLOv8 model for object detection
model = YOLO('yolov8m.pt')

# Initialize ByteTrack tracker for tracking detected objects
tracker = sv.ByteTrack()

# Initialize annotators for drawing bounding boxes and labels
box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()

def callback(frame: np.array, _: int):
    """
    Callback function to process each frame of the video.
    
    Args:
        frame (np.array): The current video frame to be processed.
        _ (int): Frame index (not used in this function).

    Returns:
        np.array: Annotated video frame with bounding boxes and labels.
    """
    # Perform object detection on the frame, focusing on class 3 (motorcycles)
    results = model(frame, classes=3)[0]
    
    # Convert detection results to a format compatible with the tracker
    detections = sv.Detections.from_ultralytics(results)
    
    # Update tracker with current detections
    detections = tracker.update_with_detections(detections)
    
    # Generate labels for detected objects, changing 'motorcycle' to 'moto'
    labels = [
        f"#{tracker_id} {'moto' if results.names[class_id] == 'motorcycle' else results.names[class_id]}"
        for class_id, tracker_id in 
        zip(detections.class_id, detections.tracker_id) 
    ]
    
    # Annotate the frame with bounding boxes
    annotated_frame = box_annotator.annotate(
        frame.copy(), detections=detections
    )
    
    # Annotate the frame with labels
    return label_annotator.annotate(
        annotated_frame, detections=detections, labels=labels
    )

# Process the video, applying the callback function to each frame
sv.process_video(
    source_path='2024-05-28-16-36-40.mp4',
    target_path='result2.mp4',
    callback=callback
)
