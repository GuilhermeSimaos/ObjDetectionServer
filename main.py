import cv2
import numpy as np
import os
import asyncio

from quart import Quart, request, send_file, render_template
from quart_cors import cors

app = Quart(__name__)
app = cors(app, allow_origin="*")

temporary_files = []
original_image_path = os.getcwd() + '/images/my-photo.jpg'
processed_image_path = os.getcwd() + '/images/processed-photo.jpg'

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


@app.route('/')
async def index():
    index_path = 'index.html'
    return await render_template(index_path)


# # Function to process image in background
# def process_image(image_path):
#     obj_detection_opencv.process_image(image_path)
#

# Async function to call process image
async def process_image_async(image_path):
    img = cv2.imread(image_path)        # Read an image

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
    cv2.imwrite((os.getcwd() + '/processed-photo.jpg'), img)


@app.route('/post-photo', methods=['POST'])
async def handle_image():
    multipart = await request.files
    image_file = multipart.get('image')

    if image_file is None:
        return 'Image not found in form', 400

    # Save file in disc and temp array for later removal
    image_file.save(original_image_path)
    temporary_files.append(original_image_path)

    # Create task for async function
    asyncio.create_task(process_image_async(original_image_path))

    return 'Image received successfully!', 200


@app.route('/get-processed-photo', methods=['GET'])
async def send_processed_photo_async():
    temporary_files.append(processed_image_path)

    while not os.path.exists(processed_image_path):
        await asyncio.sleep(0.1)

    return await send_file(processed_image_path, mimetype='image/jpg')


@app.route('/delete-files', methods=['DELETE'])
async def delete_files():
    for file_path in temporary_files:
        os.remove(file_path)

    temporary_files.clear()

    return 'Files deleted successfully!', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
