from tensorflow.keras.models import load_model
import cv2
import numpy as np
import os
from dotenv import load_dotenv


load_dotenv()

_64_squares = os.getenv("64_SQUARES_DIR")

model = load_model('chess_pieces_classifier_with_dropout.h5')

def preprocess_image(image_path, img_size=100):
    img = cv2.imread(image_path, cv2.IMREAD_ANYCOLOR)
    img_resized = cv2.resize(img, (img_size, img_size))
    img_normalized = img_resized.astype('float32') / 255.0
    img_expanded = np.expand_dims(img_normalized, axis=0)
    return img_expanded


class_order = ["A", "B", "C", "D", "E", "F", "G", "H"]
output_folder = f'{_64_squares}'

def get_chess_board_predictions():
    board_predictions = {}
    
    a = 1
    b = 0
        
    for i in range(1, 65):
        
        CATEGORIES = ["bb", "bk", "bn", "bp", "bq", "br", "wb", "wk", "wn", "wp", "wq", "wr", "zEmpty"]
        test_image_path = f'{output_folder}/{class_order[b]}{a}.png'
        a += 1
        if a == 9:
            b += 1
            a = 1
        test_image = preprocess_image(test_image_path)
        prediction = model.predict(test_image)
        predicted_class = np.argmax(prediction)
        predicted_class_name = CATEGORIES[predicted_class]
        confidence = prediction[0][predicted_class]
        board_predictions[test_image_path] = predicted_class_name
    return board_predictions



