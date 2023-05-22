import cv2
import numpy as np
import os

from flask import Flask, request, send_file
from flask_cors import CORS

# Define Flask and CORS
app = Flask(__name__)
CORS(app)

# Setting up openCV model
config_file = os.getcwd() + '/opencvFiles/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
frozen_model = os.getcwd() + '/opencvFiles/frozen_inference_graph.pb'
model = cv2.dnn_DetectionModel(frozen_model, config_file)

# Reading the classes from model classes file
class_Labels = np.array
with open((os.getcwd() + '/opencvFiles/coco.names'), 'rt') as fpt:
    class_Labels = fpt.read().rstrip('\n').split('\n')

# Setting up color scheme
np.random.seed(543210)
colors = np.random.uniform(0, 255, size=(len(class_Labels), 3))

# Configuring detection model input
model.setInputSize(320, 320)
model.setInputScale(1.0 / 127.5)
model.setInputMean((127.5, 127.5, 127.5))
model.setInputSwapRB(True)


# Responsible for processing the image
def process_image(image_path):
    # Reads an image
    img = cv2.imread(image_path)

    if img is None or img.size == 0:
        return f"Failed to load image: {image_path}"

    # Detecting objects whose confidence values are above 55%
    ClassIndex, confidence, bbox = model.detect(img, confThreshold=0.55)

    # Setting up text style
    font_scale = 2
    font = cv2.FONT_HERSHEY_PLAIN

    # Writing boxes and text of the detected objects in the image
    for ClassInd, conf, boxes in zip(ClassIndex.flatten(), confidence.flatten(), bbox):
        cv2.rectangle(img, boxes, colors[ClassInd], 2)
        cv2.putText(img, class_Labels[ClassInd - 1].upper(), (boxes[0] + 10, boxes[1] + 40), font,
                    fontScale=font_scale, color=colors[ClassInd], thickness=2)

    # Saving image in specified folder
    cv2.imwrite(os.getcwd() + '/processed-photo.jpg', img)


# Responsible for receiving and saving image locally
@app.route('/post-photo', methods=['POST'])
def handle_image():
    # Retrieving the POST image formData from frontend
    image = request.files.get('image')

    # Return error if image wasn't on the formData
    if image is None:
        return 'Image not found in form', 400

    # Saving image locally
    image.save(os.getcwd() + '/my-photo.jpg')

    # Processing image
    process_image(os.getcwd() + '/my-photo.jpg')

    # Return received image message
    return 'Image received successfully!', 200


# Endpoint for sending the processed photo
@app.route('/get-processed-photo', methods=['GET'])
def send_processed_photo():
    return send_file(os.getcwd() + '/processed-photo.jpg', mimetype='image/jpg')


@app.route('/delete-files', methods=['DELETE'])
def delete_files():
    os.remove(os.getcwd() + '/my-photo.jpg')
    os.remove(os.getcwd() + '/processed-photo.jpg')
    return "Deletion of files executed!", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
