
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid
import cv2
import numpy as np
from db_operations import insert_image, insert_circle, get_circles, get_circle
import torch

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Load YOLOv5 model
model = torch.hub.load("ultralytics/yolov5","custom", path="yolov5/runs/train/exp/weights/bests.pt")

def detect_circular_objects(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found.")
        return None, None, None

    # Run YOLOv5 model on the image
    results = model(image)
    bbox_list = results.xyxy[0].cpu().numpy()  # Extract bounding boxes (x1, y1, x2, y2, confidence, class)


    mask = np.zeros_like(image[:, :, 0])  # Initialize mask with zeros
    circles_data = []

    for bbox in bbox_list:
        x1, y1, x2, y2, conf, cls = bbox
        if conf > 0.5:  # Confidence threshold
            # Calculate centroid and radius
            x_center = int((x1 + x2) / 2)
            y_center = int((y1 + y2) / 2)
            radius = int((x2 - x1) / 2)
            cv2.circle(mask, (x_center, y_center), radius, 255, -1)
            circles_data.append({
                'id': len(circles_data),
                'bounding_box': (int(x1), int(y1), int(x2), int(y2)),
                'centroid': (x_center, y_center),
                'radius': radius
            })
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

    return image, mask, circles_data

@app.route('/')
def index():
    return render_template('index.html')

def convert_int32_to_int(data):
    if isinstance(data, np.int32):
        return int(data)
    elif isinstance(data, dict):
        return {k: convert_int32_to_int(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_int32_to_int(i) for i in data]
    else:
        return data

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the image and store results
        image_id = str(uuid.uuid4())
        original_image, mask_image, circles_info = detect_circular_objects(filepath)
        
        if original_image is None:
            return jsonify({'error': 'Image processing failed'}), 500

        # Save the processed images
        detected_filename = f"detected_{filename}"
        mask_filename = f"mask_{filename}"
        detected_filepath = os.path.join(app.config['UPLOAD_FOLDER'], detected_filename)
        mask_filepath = os.path.join(app.config['UPLOAD_FOLDER'], mask_filename)
        cv2.imwrite(detected_filepath, original_image)
        cv2.imwrite(mask_filepath, mask_image)

        # Convert int32 to int
        circles_info = convert_int32_to_int(circles_info)

        # Save image and circles info to the database
        insert_image(image_id, filename, filepath)
        for circle in circles_info:
            insert_circle(image_id, circle['bounding_box'], circle['centroid'], circle['radius'])

        response = {
            'image_id': image_id,
            'filename': filename,
            'detected_filename': detected_filename,
            'mask_filename': mask_filename,
            'circles': circles_info
        }

        return jsonify(response)

    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/circles/<image_id>', methods=['GET'])
def list_circles(image_id):
    circles = get_circles(image_id)
    return jsonify(circles)

@app.route('/circle/<image_id>/<circle_id>', methods=['GET'])
def get_circle_details(image_id, circle_id):
    circle = get_circle(image_id, circle_id)
    if circle:
        return jsonify(circle)
    return jsonify({'error': 'Circle not found'}), 404

if __name__ == '__main__':
    from db_operations import init_db
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
