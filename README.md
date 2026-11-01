# test-crane-yolo

## Overview

This project uses YOLOv8 object recognition and controls the CRANE+ robot arm.

## Behavior

- bottle -> move left
- car -> move right

## Run

bottle:

ros2 run test_pkg detect_and_move /home/ubuntu/pai_ws/images/bottle.jpg

car:

ros2 run test_pkg detect_and_move /home/ubuntu/pai_ws/images/car.jpg
