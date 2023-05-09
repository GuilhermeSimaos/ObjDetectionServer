from flask import Flask, request, send_file, render_template
from flask_cors import CORS
import obj_detection_opencv
import os

# Define Flask and CORS
app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    index_path = 'index.html'
    return render_template(index_path)


@app.route('/post-photo', methods=['POST'])
def handle_image():
    # Retrieving the POST image formData from frontend
    image = request.files.get('image')

    # Return error if image wasn't on the formData
    if image is None:
        return 'Image not found in form', 400

    # Saving image locally
    image.save(os.getcwd()+'/my-photo.jpg');

    # Processing image
    obj_detection_opencv.process_image(os.getcwd()+'/my-photo.jpg')

    # Return received image message
    return 'Image received successfully!', 200


# Endpoint for sending the processed photo
@app.route('/get-processed-photo', methods=['GET'])
def send_processed_photo():
    processed_image_path = os.getcwd()+'/processed-photo.jpg'
    return send_file(processed_image_path, mimetype='image/jpg')


if __name__ == '__main__':
    app.run(host='0.0.0.0:$PORT')
