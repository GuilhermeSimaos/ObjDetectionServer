import os
import obj_detection_opencv

from flask import Flask, request, send_file
from flask_cors import CORS

# Define Flask and CORS
app = Flask(__name__)
CORS(app)


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
    obj_detection_opencv.process_image(os.getcwd() + '/my-photo.jpg')

    # Return received image message
    return 'Image received successfully!', 200


# Endpoint for sending the processed photo
@app.route('/get-processed-photo', methods=['GET'])
def send_processed_photo():
    return send_file(os.getcwd() + '/processed-photo.jpg', mimetype='image/jpg')


# @app.route('/delete-files', methods=['DELETE'])
# def delete_files():
#     os.remove(os.getcwd() + '/my-photo.jpg')
#     os.remove(os.getcwd() + '/processed-photo.jpg')
#     return "Deletion of files executed!", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
