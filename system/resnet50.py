import os

from tensorflow.keras.applications.resnet_v2 import ResNet50V2, ResNet101V2, ResNet152V2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np

model = ResNet50V2(weights="imagenet")

def get_model():
  model_complexity = int(os.environ['MODEL_SIZE'])

  if model_complexity == 50:
    return ResNet50V2(weights="imagenet")
  if model_complexity == 101:
    return ResNet101V2(weights="imagenet")
  if model_complexity == 152:
    return ResNet152V2(weights="imagenet")

def predict(file_path):
  img = image.load_img(file_path, target_size=(224, 224))
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)
  x = preprocess_input(x)

  preds = get_model().predict(x)
  return decode_predictions(preds, top=3)[0]