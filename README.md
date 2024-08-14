# Helmet and Number Plate Detection System

This project uses the YOLOv5 object detection model to identify three classes: rider, helmet, and number plate. The system is designed to be integrated with CCTV cameras to automate traffic rule enforcement. If a rider is detected without wearing a helmet, the system crops the license plate from the frame and uses OCR to detect and read the number plate.

## Features

- **Real-time Detection**: Detects riders, helmets, and number plates in real-time.
- **Helmet Detection**: Identifies if a rider is wearing a helmet. If not, the system flags the violation.
- **License Plate Cropping**: Crops the license plate from the image if a helmet violation is detected.
- **OCR for Number Plate**: Uses Optical Character Recognition (OCR) to read and log the number plate of the violating rider.
- **CCTV Integration**: Can be integrated with existing CCTV camera systems for continuous monitoring.


## Setup and Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/styloo007/licenceplate-detection-YOLOv5.git
    cd licenceplate-detection-YOLOv5
    ```

2. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
