# Perception

This guide explains how the perception stack is organized and how object detection is performed using **YOLO** within the Autonomous Mobile Robot project.

The perception package is responsible for processing camera images, detecting objects, and publishing annotated images and structured detection data for the rest of the robot.

---

# Table of Contents

- Overview
- Package Structure
- Perception Pipeline
- Requirements
- Installing Dependencies
- YOLO
- Launching the Perception Stack
- Topics
- Parameters
- Validation
- Troubleshooting
- Future Improvements

---

# Overview

The perception package performs real-time object detection using a monocular RGB camera.

The current implementation is based on **Ultralytics YOLO** and is designed to remain lightweight while being easily replaceable by more optimized inference engines (ONNX, NCNN, TensorRT) in the future.

Current features:

- RGB image acquisition
- Real-time object detection
- Annotated debug image publication
- Configurable confidence threshold
- Adjustable inference frequency
- Modular ROS 2 node architecture

---

# Package Structure

```
amr_perception/

├── config/
│   └── perception.yaml
│
├── launch/
│   └── perception.launch.py
│
├── amr_perception/
│   ├── __init__.py
│   └── yolo_detector_node.py
│
├── package.xml
└── setup.py
```

---

# Perception Pipeline

```
Gazebo Camera
       │
       ▼
/camera/image
       │
       ▼
cv_bridge
       │
       ▼
OpenCV Image
       │
       ▼
YOLO
       │
       ▼
Object Detections
       │
       ├──────────────► Bounding Boxes
       │
       ▼
Annotated Image
       │
       ▼
/perception/debug_image
```

---

# Requirements

The perception package depends on:

- ROS 2 Jazzy
- OpenCV
- cv_bridge
- vision_msgs
- image_transport
- Ultralytics YOLO
- PyTorch

---

# Installing Dependencies

Install the required ROS packages:

```bash
sudo apt update

sudo apt install \
    ros-jazzy-rqt-image-view \
    ros-jazzy-cv-bridge \
    ros-jazzy-vision-msgs \
    ros-jazzy-ros-gz-image
```

Install the Python dependencies:

```bash
pip install ultralytics
```

If using a virtual environment:

```bash
source .venv/bin/activate

pip install ultralytics
```

---

# YOLO

The perception node currently uses **Ultralytics YOLO** for real-time object detection.

YOLO (You Only Look Once) is a single-stage object detector capable of detecting multiple objects in a single forward pass.

Advantages:

- High detection speed
- Low latency
- Real-time inference
- Easy export to embedded inference engines
- Large ecosystem

Current workflow:

```
Camera Image

↓

YOLO

↓

Bounding Boxes

↓

Annotated Image

↓

ROS Topic
```

The detector loads a pretrained model at startup:

```python
self.model = YOLO(model_path)
```

Each incoming image is converted into an OpenCV image using `cv_bridge`, processed by YOLO, then published as an annotated debug image.

---

# Current Model

Current model:

```
YOLO26n
```

Reasons for this choice:

- Lightweight
- Good accuracy
- Fast CPU inference
- Suitable for Raspberry Pi deployment
- Easy export to ONNX

The model can easily be replaced in `perception.yaml`.

Example:

```yaml
model: yolo26n.pt
```

---

# Detection Parameters

Typical parameters:

```yaml
confidence: 0.40

inference_rate: 5.0

device: cpu
```

Description:

| Parameter | Description |
|-----------|-------------|
| model | YOLO model path |
| confidence | Minimum detection confidence |
| inference_rate | Maximum inference frequency |
| device | cpu or cuda |

---

# Launching the Perception Stack

Launch only the perception package:

```bash
ros2 launch amr_perception perception.launch.py
```

---

# Topics

Input image:

```
/camera/image
```

Annotated image:

```
/perception/debug_image
```

Future versions will also publish:

```
/perception/detections
```

using `vision_msgs`.

---

# Validation

Verify the node:

```bash
ros2 node list
```

Expected:

```
/yolo_detector
```

---

Verify the debug topic:

```bash
ros2 topic list
```

Expected:

```
/perception/debug_image
```

---

Monitor the output frequency:

```bash
ros2 topic hz /perception/debug_image
```

---

Display the annotated image:

```bash
rqt_image_view
```

Select:

```
/perception/debug_image
```

---

# Parameters

List the parameters:

```bash
ros2 param list /yolo_detector
```

Read a parameter:

```bash
ros2 param get /yolo_detector confidence
```

---

# Troubleshooting

## No image received

Verify:

```bash
ros2 topic list
```

The camera topic should exist.

---

## No detections

Possible causes:

- confidence threshold too high
- unsupported object
- poor lighting
- unrealistic Gazebo textures

Reduce the confidence threshold:

```yaml
confidence: 0.25
```

---

## Wrong detections

Gazebo models can sometimes generate false positives because YOLO has been trained on the COCO dataset.

Examples:

- airplane
- stop sign

This is expected when the detector encounters synthetic environments.

---

## Low frame rate

Reduce:

- image resolution
- camera frame rate
- inference frequency

Example:

```yaml
inference_rate: 5.0
```

---

## CPU usage too high

Possible optimizations:

- use a smaller YOLO model
- reduce image resolution
- decrease inference frequency
- export the model to ONNX
- use NCNN or TensorRT on embedded hardware

---

# Future Improvements

The perception stack has been designed to remain modular.

Planned improvements include:

- Detection2DArray publication (`vision_msgs`)
- Person-only detection mode
- Object tracking
- Multi-camera support
- ONNX Runtime inference
- NCNN deployment for Raspberry Pi
- TensorRT acceleration
- Depth estimation
- Semantic segmentation
- 3D object localization
- Human detection for autonomous navigation
- Dynamic obstacle tracking