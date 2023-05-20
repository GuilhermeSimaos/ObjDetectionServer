from quart import Quart, request, send_file, render_template
from quart_cors import cors
import obj_detection_opencv
import os
import asyncio

app = Quart(__name__)
app = cors(app, allow_origin="*")

temporary_files = []


async def process_image_async(image_path):
    await asyncio.to_thread(obj_detection_opencv.process_image, image_path)


@app.route('/')
async def index():
    index_path = 'index.html'
    return await render_template(index_path)


@app.route('/post-photo', methods=['POST'])
async def handle_image():
    form = await request.form
    image = form.get('image')

    if image is None:
        return 'Image not found in form', 400

    original_image_path = os.getcwd() + '/my-photo.jpg'

    with open(original_image_path, 'wb') as f:
        f.write(image)

    temporary_files.append(original_image_path)

    asyncio.create_task(process_image_async(original_image_path))

    return 'Image received successfully!', 200


@app.route('/get-processed-photo', methods=['GET'])
async def send_processed_photo_async():
    processed_image_path = os.getcwd() + '/processed-photo.jpg'

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
