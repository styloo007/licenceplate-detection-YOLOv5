import subprocess
import os
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import torch
from PIL import Image
from yolov5.models.common import Detections
import cv2
import os
import mysql.connector
import base64
from datetime import datetime
import easyocr

def index(request):
    return render(request, 'index.html')


globalimg=""



def predict(request):
    
    if request.method == 'POST':
        uploaded_image = request.FILES['image_input']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_image.name, uploaded_image)

        # Ensure temporary file path construction:
        image_path = os.path.join(settings.MEDIA_ROOT, filename)
        
        
        
        def is_inside(box1, box2, threshold=0.3):
            """
            Checks if box1 is mostly inside box2.

            Args:
                box1: A dictionary containing 'xmin', 'ymin', 'xmax', and 'ymax' keys.
                box2: A dictionary containing 'xmin', 'ymin', 'xmax', and 'ymax' keys.
                threshold: The threshold percentage of box1 inside box2 to consider as inside.

            Returns:
                True if box1 is mostly inside box2, False otherwise.
            """
            # Calculate the area of box1
            area_box1 = (box1['xmax'] - box1['xmin']) * (box1['ymax'] - box1['ymin'])

            # Calculate the area of intersection between box1 and box2
            inter_area = max(0, min(box1['xmax'], box2['xmax']) - max(box1['xmin'], box2['xmin'])) * \
                         max(0, min(box1['ymax'], box2['ymax']) - max(box1['ymin'], box2['ymin']))

            # Calculate the percentage of box1 inside box2
            overlap_percentage = inter_area / area_box1

            return overlap_percentage >= threshold
        
        # Path to weights file
        weights_path = '1500img.pt'

        # Load the model
        model = torch.hub.load('', 'custom', path=weights_path, source='local')
        

        # Perform inference
        output = model(image_path,416)
        
        
        
        result = subprocess.run([
                "python",
                "yolov5/detect2.py",
                "--weights", "1500img.pt",
                "--source", image_path,
                "--img", "416"
            ], capture_output=True, text=True)  
        
        
        


        # Get bounding boxes and class names
        boxes = output.pandas().xyxy[0].to_dict('records')
        class_names = output.pandas().names[0] if output.pandas().names else [f"box_{i+1}" for i in range(len(boxes))]

        # Find rider and helmet bounding boxes
        rider_boxes = [box for box in boxes if box['name'] == "rider"]
        helmet_boxes = [box for box in boxes if box['name'] == "helmet"]
        license_plate_boxes = [box for box in boxes if box['name'] == "plate"]

        # Check for helmet inside each rider box
        rider_count = 1
        for rider_box in rider_boxes:
            helmet_found = False
            for helmet_box in helmet_boxes:
                if is_inside(helmet_box, rider_box, threshold=0.3):
                    helmet_found = True
                    break
                
            if not helmet_found:
                print(f"No helmet found for rider {rider_count}")

                # If no helmet found, find license plate inside the rider's box and crop it
                for plate_box in license_plate_boxes:
                    if is_inside(plate_box, rider_box):
                        # Crop the license plate from the image
                        img = Image.open(image_path)
                        plate_img = img.crop((plate_box['xmin'], plate_box['ymin'], plate_box['xmax'], plate_box['ymax']))
                        # Save cropped image with filename
                        plate_img.save(f"E:/Haegl/lpUI/LP_CROPS/rider_{rider_count}_plate.jpg")
                        print(f"License plate cropped for rider {rider_count}")

            rider_count += 1
            
            
        # Initialize the EasyOCR reader
        reader = easyocr.Reader(['en'])

        # Path to the cropped license plate image
        plate_image_path = "E:/Haegl/lpUI/LP_CROPS/rider_1_plate.jpg"  # Adjust the path accordingly

        # Read text from the license plate image
        result = reader.readtext(plate_image_path)
        
        platereading="Vehicle Without Helmet Identified: "

        for detections in result:
            platereading+=detections[1]
            print(detections[1])
            
        
        
        
            
            
        # Remove the image file after processing
        os.remove(image_path)
        
        
        # Get the latest saved image path in the static folder
        latest_image_path = os.path.join(settings.STATIC_URL, filename)
        
        
        



        

        # Render results
        params = {'img_pth': latest_image_path, 'platereading':platereading}
        return render(request, 'result.html', params)
        

def delete(request):
    return render(request, 'index.html')
