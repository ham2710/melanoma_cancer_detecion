from tensorflow.keras.models import load_model

loaded_model = load_model('inputs/skin_cancer_model.h5')

# Assuming you have an image 'test_image.jpg' for prediction
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

class_names = ['Actinic Keratosis',
                'Basal Cell Carcinoma',
                'Dermatofibroma',
                'Melanoma',
                'Nevus',
                'Pigmented Benign Keratosis',
                'Seborrheic Keratosis',
                'Squamous Cell Carcinoma',
                'Vascular Lesion','NONE']

def predict_cancer(image_name):
    print(image_name)
    test_image = load_img(image_name, target_size=(180, 180))
    test_image = img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)

    prediction = loaded_model.predict(test_image)
    predicted_class_index = np.argmax(prediction)
    predicted_class = class_names[predicted_class_index]

    print("Predicted Class:", predicted_class)
    return predicted_class


