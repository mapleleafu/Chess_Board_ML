from PIL import Image
from crop_the_screenshot import crop_chessboard
from dotenv import load_dotenv
import os

load_dotenv()

Chess_Board_ML = os.getenv("Chess_Board_ML_DIR")
_64_squares = os.getenv("64_squares_DIR")

def crop_chess_board_squares(input_image_path, output_folder, square_size=0):
    #!                                                      DONT FORGET TO CHANGE
    image = Image.open(input_image_path)
    width, height = image.size
    square_width, square_height = square_size, square_size
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", ]
    for i in range(0, 8):
        count = 1
        for j in range(0, 8):
            left = j * square_width
            upper = i * square_height
            right = left + square_width
            lower = upper + square_height

            cropped_square = image.crop((left, upper, right, lower))

            output_file_name = f"{output_folder}/{letters[j]}{8 - i}.png"
            cropped_square.save(output_file_name)
            count += 1


if __name__ == '__main__':
    screenshot_path = f'{Chess_Board_ML}screenshot.png'
    input_image_path = f'{Chess_Board_ML}cropped_chessboard.png'
    output_folder = f'{_64_squares}'

    dimensions = crop_chessboard(screenshot_path)
    
    if dimensions is not None:
        width, height = dimensions
        square_size = width // 8
        crop_chess_board_squares(input_image_path, output_folder, square_size)
    else:
        print("Failed to get dimensions.")


