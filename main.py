import anyio.to_thread
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
import obj_detection_opencv

# Define FastAPI app
app = FastAPI()


@app.get('/')
async def index():
    index_path = 'index.html'
    return FileResponse(index_path)


@app.post('/post-photo')
async def handle_image(image: UploadFile = File(...)):
    # Return error if image wasn't uploaded
    if image is None:
        return 'Image not found in form', 400

    # Saving locally
    with open(os.getcwd() + '/my-photo.jpg', 'wb') as f:
        f.write(await image.read())

    # Processing image asynchronously
    await anyio.to_thread.run_sync(
        obj_detection_opencv.process_image,
        os.getcwd() + '/my-photo.jpg'
    )

    # Return received image message
    return 'Image received successfully!', 200


# Endpoint for sending the processed photo
@app.get('/get-processed-photo')
async def send_processed_photo():
    processed_image_path = os.getcwd()+'/processed-photo.jpg'
    return FileResponse(processed_image_path, media_type='image/jpg')


# Responsible for deleting images saved locally
@app.delete('/delete-files')
async def delete_files():
    if os.path.exists(os.getcwd() + '/my-photo.jpg'):
        os.remove(os.getcwd() + '/my-photo.jpg')

    if os.path.exists(os.getcwd() + '/processed-photo.jpg'):
        os.remove(os.getcwd() + '/processed-photo.jpg')

    return "Deletion of files executed!", 200


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0')
