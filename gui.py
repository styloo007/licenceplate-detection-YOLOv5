import tkinter as tk
from tkinter import filedialog, scrolledtext
import subprocess

# Function to perform YOLOv5 object detection
def perform_object_detection(image_path):
    result = subprocess.run([
        "python",
        "yolov5/detect2.py",
        "--weights", "1500img.pt",
        "--source", image_path,
        "--img", "416"
    ], capture_output=True, text=True)
    return result.stdout

# Function to handle image upload and object detection
def upload_and_detect():
    filename = filedialog.askopenfilename()
    if filename:
        output_text.delete(1.0, tk.END)  # Clear previous output
        output = perform_object_detection(filename)
        output_text.insert(tk.END, output)

# Create Tkinter GUI
root = tk.Tk()
root.title("YOLOv5 Object Detection")

# Create and configure upload button
upload_button = tk.Button(root, text="Upload Image", command=upload_and_detect)
upload_button.pack()

# Create and configure text widget to display output
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
output_text.pack()

root.mainloop()
