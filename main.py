from flask import Flask, request, send_file, render_template
from flask_cors import CORS
import obj_detection_opencv
import os
import asyncio

# Define Flask and CORS
app = Flask(__name__)
CORS(app)

temporary_files = []


async def process_image_async(image_path):
    await asyncio.to_thread(obj_detection_opencv.process_image, image_path)


@app.route('/')
def index():
    index_path = 'index.html'
    return render_template(index_path)


@app.route('/post-photo', methods=['POST'])
def handle_image():
    # Retrieving the POST image formData from frontend
    image = request.files.get('image')

    # Return error if image wasn't in the formData
    if image is None:
        return 'Image not found in form', 400

    # Setting the original image path variable
    original_image_path = os.getcwd() + '/my-photo.jpg'

    # Saving the image locally and temporarily
    image.save(original_image_path)
    temporary_files.append(original_image_path)

    # Processing the image using the async function
    asyncio.create_task(process_image_async(original_image_path))

    # Return the received image message
    return 'Image received successfully!', 200


# Endpoint for sending the processed photo
@app.route('/get-processed-photo', methods=['GET'])
async def send_processed_photo_async():
    # Setting processed image path
    processed_image_path = os.getcwd() + '/processed-photo.jpg'

    # Adding processed image to temp array for deletion
    temporary_files.append(processed_image_path)

    while not os.path.exists(processed_image_path):
        await asyncio.sleep(0.1)

    return send_file(processed_image_path, mimetype='image/jpg')


# Endpoint deleting images
@app.route('/delete-files', methods=['DELETE'])
def delete_files():
    # Using OS to remove saved images
    for file_path in temporary_files:
        os.remove(file_path)

    temporary_files.clear()

    return 'Files deleted successfully!', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
