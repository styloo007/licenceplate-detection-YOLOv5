import torch
import sys

model = torch.hub.load()

img_path='Screenshot 2024-02-27 172328_SAu1DqF.png'

# Perform inference on the image
result = model(img_path)

# Display the results
result.show()
