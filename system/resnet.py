from PIL import ImageFile
from tensorflow.keras.applications.resnet_v2 import ResNet50V2, ResNet101V2, ResNet152V2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np

class ResNet():
  _instance = None
  _num = 0

  def __new__(cls, depth):
    if cls._instance is None:
      ImageFile.LOAD_TRUNCATED_IMAGES = True
      cls._instance = super(ResNet, cls).__new__(cls)

      if depth == 50:
        cls.model = ResNet50V2(weights="imagenet")
      elif depth == 101:
        cls.model = ResNet101V2(weights="imagenet")
      elif depth == 152:
        cls.model = ResNet152V2(weights="Imagenet")
      else:
        raise Exception("Unknown Model")

    return cls._instance
  
  def predict(self, file_path):
    img = image.load_img(file_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = self.model.predict(x)
    return decode_predictions(preds, top=3)[0]