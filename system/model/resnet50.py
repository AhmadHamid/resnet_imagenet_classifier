import os

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from tensorflow.keras.applications.resnet_v2 import ResNet50V2, ResNet101V2, ResNet152V2

import numpy as np

def get_model_by_environment_variable():
    if 'MODEL_SIZE' not in os.environ:
        print("Take model 50")
        return ResNet50V2(weights="imagenet")
    model_size = os.environ['MODEL_SIZE']
    if model_size == "50":
        print("Take model 50")
        return ResNet50V2(weights="imagenet")
    elif model_size == "101":
        print("Take model 101")
        return ResNet101V2(weights="imagenet")
    elif model_size == "152":
        print("Take model 152")
        return ResNet152V2(weights="imagenet")


def predict(file_path):
    img = image.load_img(file_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    model = get_model_by_environment_variable()
    predictions = model.predict(x)
    return decode_predictions(predictions, top=3)
