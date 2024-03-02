import tkinter as tk
import subprocess
import chess
from tkinter import ttk
from screenshot import grab_screen
from crop_the_screenshot import crop_chessboard
from square_make import square_maker


def main():
    run_mainloop()

def screenshot_button_click(screenshot_error_label):
    try:
        img = grab_screen()
        cropped_img = crop_chessboard(img)
        square_maker(img, cropped_img)
        output = subprocess.check_output(["python", "board_display_and_actions.py"], stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
        screenshot_error_label.config(text="")
        return True
    except subprocess.CalledProcessError as e:
        output = e.output
        print(f"An error occurred: {output}")
        screenshot_error_label.config(text="Opera Is Not Open!", fg="red")
        return False


def fen_button_click(fen, fen_error_label, fen_entry):
    board = chess.Board()
    try:
        board.set_fen(fen)
        print("Valid FEN code.")
        subprocess.run(["python", "board_display_and_actions.py", fen])
        fen_error_label.config(text="")
        return True
    except ValueError:
        print("Error: Invalid FEN code.")
        fen_error_label.config(text="Invalid FEN position", fg="red")
        fen_entry.delete(0, tk.END)
        return False


def run_mainloop():
    root = tk.Tk()
    root.title("Chess")
    root.geometry("300x190")

    take_screenshot_button = ttk.Button(root, text="Take a Screenshot", command=lambda: screenshot_button_click(screenshot_error_label))
    take_screenshot_button.pack(pady=10)

    screenshot_error_label = tk.Label(root, text="", fg="red")
    screenshot_error_label.pack(pady=10)

    fen_entry = tk.Entry(root, width=40)
    fen_entry.pack(pady=5)

    fen_button = ttk.Button(root, text="Load FEN", command=lambda: fen_button_click(fen_entry.get(), fen_error_label, fen_entry))
    fen_button.pack(pady=5)

    fen_error_label = tk.Label(root, text="", fg="red")
    fen_error_label.pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()