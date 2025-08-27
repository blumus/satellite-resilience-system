from ultralytics import YOLO
import urllib.request
import os

# Download a sample image
image_url = 'https://ultralytics.com/images/bus.jpg'
image_file = 'bus.jpg'
urllib.request.urlretrieve(image_url, image_file)
print(f"Downloaded image: {image_file}")

# Load a pretrained YOLOv8 model
print("Loading YOLOv8 model...")
model = YOLO('yolov8n.pt')

# Run inference on the image
print("Running inference...")
results = model(image_file)

# Print the results
print("\n--- Detection Results ---")
for r in results:
    for box in r.boxes:
        class_id = int(box.cls)
        class_name = model.names[class_id]
        confidence = float(box.conf)
        print(f"Detected: {class_name} (Confidence: {confidence:.2f})")

# You can also save the results with bounding boxes
r.save(filename='detected_bus.jpg')
print(f"Results saved to detected_bus.jpg")
