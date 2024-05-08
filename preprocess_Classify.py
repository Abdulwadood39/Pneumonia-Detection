import tensorflow as tf
import numpy as np
from PIL import Image
from io import BytesIO


classify_model_path = "./models/vggnet_xray_classifier_model.h5"
Pneumonia_model_path = './models/PneumoXpert_VGG16.h5'



# Load the pre-trained TensorFlow model and classes for X-RAY Classifier
CLASSIFY_MODEL = tf.keras.models.load_model(classify_model_path)
CLASSIFY_CLASSES = ['Non-X-Ray', 'X-Ray']

# Load the pre-trained TensorFlow model and classes for Pneumonia Classifier
PNEUMO_MODEL = tf.keras.models.load_model(Pneumonia_model_path)
# P_classes = ['NORMAL', 'PNEUMONIA']
PNEUMO_CLASSES = ['Not Detected', 'Detected']

# Preprocess image for XRAY-classification
def preprocess_image(image):
    img = image.resize((256, 256))
    img = img.convert("RGB")
    img = np.array(img) / 255.0
    img = img.reshape(1, 256, 256, 3)
    return img


# Classify the image
def classify_image(image):
    processed_image = preprocess_image(image)
    predictions = CLASSIFY_MODEL.predict(processed_image)
    predicted_class = 0 if predictions < 0.5 else 1
    return CLASSIFY_CLASSES[predicted_class]


def decode_img(img):
    img = img.resize((128, 128))
    img = img.convert("RGB")
    img = np.array(img) / 255.0
    img = img.reshape(1, 128, 128, 3)

    return img

def classify_image_pneumo(image):
    try:
        processed_image = decode_img(image)
        predictions = PNEUMO_MODEL.predict(processed_image)
        predicted_class = np.argmax(predictions)
        return PNEUMO_CLASSES[predicted_class]
    except Exception as e:
        print("An error occurred while processing the image:", str(e))
        return "Error"
    