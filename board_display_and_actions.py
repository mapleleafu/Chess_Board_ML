import chess
import os
import tkinter as tk
import webbrowser
import sys
import os.path
from PIL import Image, ImageTk
from square_test import get_chess_board_predictions
from black_to_play import rotate_board_and_change_side
from stockfish import Stockfish
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

stockfish_dir = os.getenv("STOCKFISH_DIR")

stockfish = Stockfish(rf"{stockfish_dir}")

PIECE_MAP = {
    "bb": "b",
    "bk": "k",
    "bn": "n",
    "bp": "p",
    "bq": "q",
    "br": "r",
    "wb": "B",
    "wk": "K",
    "wn": "N",
    "wp": "P",
    "wq": "Q",
    "wr": "R",
}

white_to_play_press = False
reversed = False


if len(sys.argv) <= 1:
    predictions = get_chess_board_predictions()

    board = chess.Board.empty()

    for file_path, piece in predictions.items():
        square_name = os.path.splitext(os.path.basename(file_path))[0]  
        square_int = chess.parse_square(square_name.lower())

        if piece != "zEmpty":
            piece_symbol = PIECE_MAP[piece]
            piece_obj = chess.Piece.from_symbol(piece_symbol)
            board.set_piece_at(square_int, piece_obj)

    white_fen = board.fen()
    print(white_fen)

    black_fen = rotate_board_and_change_side(white_fen)
    print(black_fen)

else:
    def get_color_to_move(fen):
        fen_parts = fen.split()
        return fen_parts[1]
    color_to_move = get_color_to_move(sys.argv[1])
    

    if color_to_move == "w":
        white_fen = sys.argv[1]
        white_to_play_press = True
    else:
        black_fen = sys.argv[1] 
        reversed = True 


# Tkinter GUI
class ChessBoardGUI(tk.Tk):
    def __init__(self, fen, stockfish, img=None):
        super().__init__()
        self.title("Chess Board")
        self.geometry("400x480")

        self.stockfish = stockfish
        self.board = chess.Board(fen)

        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.pack()

        self.images = []

        self.draw_board()
        self.draw_pieces()

        self.button_area = tk.Frame(self, height=33, width=400)
        self.button_area.pack(fill=tk.X)

        self.left_button_frame = tk.Frame(self.button_area, height=50, width=200)
        self.left_button_frame.pack(side=tk.LEFT)

        self.analysis_button_frame = tk.Frame(self.button_area, height=50, width=200)
        self.analysis_button_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.white_to_play = tk.Button(self.left_button_frame, text="White to play", command=lambda: self.white_button_action(white_fen))
        self.white_to_play.pack(side=tk.LEFT, padx=10, pady=10)
    
        self.black_to_play = tk.Button(self.analysis_button_frame, text="Black to play", command=lambda: self.black_button_action(black_fen))
        self.black_to_play.pack(side=tk.RIGHT, padx=10, pady=10)


        if white_to_play_press == True:
            self.white_to_play.invoke()
        if reversed == True:
            self.black_to_play.invoke()

    def save_fen_history(self, fen_history):
        current_date = datetime.now().strftime("%d-%m-%Y")
        hour = datetime.now().hour
        minute = datetime.now().minute  
        filename = "fen_history.txt"

        with open(filename, "a") as f:
            for fen in fen_history:
                f.write(f"FEN: {fen} , Time: {hour}:{minute}, Date: {current_date}\n")

    def hide_history_button(self):
        self.history_button.place(x=-200, y=self.button_area['height'] - 5, width=70, height=25)


    def create_history_button(self):
        button_width = 70
        button_height = 25
        padx = 5

        if not hasattr(self, 'history_button'):  # Check if the history_button attribute exists
            self.history_button = tk.Button(self.button_area, text="FEN History", command=self.history_button_action, width=button_width, state=tk.DISABLED)
            self.history_button.place(x=padx, y=self.button_area['height'] - 5, width=button_width, height=button_height)  # Adjust the y-coordinate


    def create_evaluation_best_move_buttons(self):
        self.white_to_play.destroy()
        self.black_to_play.destroy()
        self.create_history_button()


        self.best_move = self.stockfish.get_best_move()
        self.eval = self.stockfish.get_evaluation()

        button_width = 70
        middle_button_width = 65
        button_height = 25
        padx = 5
        middle_button_space = 10
        offset = 3 # Change this value to adjust the height of the labels

        self.evaluation_button = tk.Button(self.button_area, text="Evaluation", command=self.evaluation_button_action, width=button_width)
        self.evaluation_button.place(x=padx, y=(self.button_area['height'] - button_height) // 2, width=button_width, height=button_height)

        self.evaluation_label = tk.Label(self.button_area, text="")
        self.evaluation_label.place(x=padx + button_width, y=((self.button_area['height'] - button_height) // 2) + offset)

        self.editor_button = tk.Button(self.button_area, text="Editor", command=lambda: self.editor_button_action(self.fen), width=middle_button_width)
        self.editor_button.place(x=(self.button_area['width'] - middle_button_width * 2 - middle_button_space) // 2, y=(self.button_area['height'] - button_height) // 2, width=middle_button_width, height=button_height)

        self.analysis_button = tk.Button(self.button_area, text="Analysis", command=lambda: self.analysis_button_action(self.fen), width=middle_button_width)
        self.analysis_button.place(x=(self.button_area['width'] + middle_button_space) // 2, y=(self.button_area['height'] - button_height) // 2, width=middle_button_width, height=button_height)

        self.best_move_button = tk.Button(self.button_area, text="Best move", command=self.best_move_button_action, width=button_width, fg="#000000") #fg="red" add to the end for the color
        self.best_move_button.place(x=self.button_area['width'] - button_width - padx, y=(self.button_area['height'] - button_height) // 2, width=button_width, height=button_height)

        self.best_move_label = tk.Label(self.button_area, text="")
        self.best_move_label.place(x=self.button_area['width'] - button_width * 2 - padx * 2 + 35, y=((self.button_area['height'] - button_height) // 2) + offset) 


        self.fen_history = []

    def white_button_action(self, fen):
        self.create_evaluation_best_move_buttons()
        self.fen = white_fen
        self.stockfish.set_fen_position(fen)
        self.board = chess.Board(white_fen)
        self.best_move = self.stockfish.get_best_move()
        self.eval = self.stockfish.get_evaluation()
        self.draw_pieces()
        self.history_button.config(state=tk.NORMAL)  # Enable the FEN History button
        self.fen_history.append(self.fen)  # Add this line to append the current FEN to the history list
        self.save_fen_history(self.fen_history)


    def black_button_action(self, fen):
        self.create_evaluation_best_move_buttons()
        self.fen = black_fen
        self.stockfish.set_fen_position(fen)
        self.board = chess.Board(black_fen)
        self.best_move = self.stockfish.get_best_move()
        self.eval = self.stockfish.get_evaluation()
        self.draw_pieces()
        self.history_button.config(state=tk.NORMAL)  # Enable the FEN History button
        self.fen_history.append(self.fen)  # Add this line to append the current FEN to the history list
        self.save_fen_history(self.fen_history)


    def evaluation_button_action(self):
        print("Evaluation button clicked!")
        self.eval = self.stockfish.get_evaluation()
        if self.eval['type'] == "cp":
            self.evaluation_label.config(text=self.eval['value'] / 100, fg="blue")
        else:
            _ = self.eval['value']
            _ = str(_)
            if "-" in _:
                _ = _.replace("-", "")
            text1 = f"{self.eval['type'].capitalize()} in {_}"
            self.evaluation_label.config(text=text1, fg="green")


    def best_move_button_action(self):
        print("Best move button clicked!")
        self.best_move = self.stockfish.get_best_move()
        self.best_move_label.config(text=self.best_move, fg="green")


    def analysis_button_action(self,fen):
        print("analysis button clicked!")
        fen_with_underscores = fen.replace(" ", "_")
        url = f"https://lichess.org/analysis/{fen_with_underscores}"
        webbrowser.open_new_tab(url)


    def editor_button_action(self, fen):
        print("Editor button clicked!")
        fen_with_underscores = fen.replace(" ", "_")
        url = f"https://lichess.org/editor/{fen_with_underscores}"
        webbrowser.open_new_tab(url)


    def history_button_action(self):
        print("History button clicked!")
        history_window = tk.Toplevel(self)
        history_window.title("FEN History")
        history_window.geometry("600x300")

        scrollbar = tk.Scrollbar(history_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        history_listbox = tk.Listbox(history_window, yscrollcommand=scrollbar.set)
        
        # Read the FEN history from the file
        filename = "fen_history.txt"
        if os.path.isfile(filename):
            with open(filename, "r") as f:
                for line in f:
                    date_and_fen = line.strip()
                    history_listbox.insert(tk.END, date_and_fen)

        history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=history_listbox.yview)



    def draw_board(self):
        colors = ["white", "light gray"]
        square_size = 400 // 8
        for i in range(8):
            for j in range(8):
                color = colors[(i + j) % 2]
                self.canvas.create_rectangle(
                    i * square_size, j * square_size, (i + 1) * square_size, (j + 1) * square_size, fill=color
                )


    def draw_pieces(self):
        self.canvas.delete("all")  # Add this line to clear the canvas
        self.draw_board()  # Add this line to redraw the board
        square_size = 400 // 8
        for i in range(64):
            piece = self.board.piece_at(i)
            if piece:
                piece_color = "w" if piece.color == chess.WHITE else "b"
                image_path = f"images_for_board_display/{piece_color}{piece.symbol().upper()}.png"
                image = Image.open(image_path)
                image = image.resize((square_size, square_size), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                if self.board.turn == chess.BLACK:
                    i = 63 - i

                self.canvas.create_image(
                    (i % 8) * square_size + square_size / 2,
                    (7 - i // 8) * square_size + square_size / 2,
                    image=photo,
                )
                self.images.append(photo)  # Add this line to store the image reference in the list
        

if __name__ == "__main__":
    fen = sys.argv[1] if len(sys.argv) > 1 else white_fen
    app = ChessBoardGUI(fen, stockfish)
    app.mainloop()

