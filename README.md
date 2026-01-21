# Stretching Assistant

Experimental tool for visual stretching assistance based on pose estimation.  
It allows you to **start the camera**, **detect body keypoints**, and **calculate angles** between relevant points for posture analysis.

> ⚠️ **Incomplete / inactive project** — this repository contains prototype and research code rather than a ready-to-use solution.

---

## Motivation

The goal of this project is to experiment with a visual stretching assistant that:

- captures the webcam in real-time  
- detects human body keypoints  
- calculates angles between body segments for posture and exercise evaluation  
- integrates simple communication with other processes (e.g., external UI, feedback modules)

The focus is on **pose estimation and angle analysis**, which are widely used techniques in computer vision fitness applications.

---

## Features

- starts the camera and displays the video feed  
- draws detected keypoints on the video frame  
- calculates angles between selected keypoints  
- includes a **communication schema with another process** for data exchange

---

## How it works

1. **Pose Estimation:** uses Google MediaPipe Pose to detect body keypoints.  
2. **Angle Calculation:** angles between specific joints (e.g., elbow, shoulder, hip) are calculated per frame.  
3. **Output:** keypoints and angles can be displayed or sent to another module via a simple inter-process communication protocol.

---

## Requirements

Ensure you have installed:

```bash
python3 >= 3.8
pip install -r requirements.txt
```
---

## Usage

1. Clone the repository and install the requirements.
2. Run the source/main.py script to open the camera and see keypoints overlaid on the video.
3. Run the source/receiver.py script to observe the calculated angles by the main process
