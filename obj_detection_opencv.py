import cv2
import numpy as np
import os

# Taking configuration and model file
config_file = os.getcwd() + '/opencvFiles/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
frozen_model = os.getcwd() + '/opencvFiles/frozen_inference_graph.pb'

# Setting up detection model
model = cv2.dnn_DetectionModel(frozen_model, config_file)

# Reading the classes from model file
class_Labels = np.array
file_name = os.getcwd() + '/opencvFiles/coco.names'
with open(file_name, 'rt') as fpt:
    class_Labels = fpt.read().rstrip('\n').split('\n')

# Setting up color scheme
np.random.seed(54321)
colors = np.random.uniform(0, 255, size=(len(class_Labels), 3))

# Configuring detection model input
model.setInputSize(320, 320)
model.setInputScale(1.0 / 127.5)
model.setInputMean((127.5, 127.5, 127.5))
model.setInputSwapRB(True)


# Function to process images and save it locally
def process_image(image_path):
    """ --------------------------------------- IMAGE ------------------------------------------------------

    This function is used to analyse an image and save the processed image in Images folder.
    The processed image will have the addition of boundary boxes with text of the detected objects in it.

    --------------------------------------------------------------------------------------------------------"""
    # Read an image information
    img = cv2.imread(image_path)

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
    processed_image = os.getcwd() + '/processed-photo.jpg'
    cv2.imwrite(processed_image, img)


# Credits to: https://www.youtube.com/watch?v=RFqvTmEFtOE
# Also : https://www.youtube.com/watch?v=lE9eZ-FGwoE
