# **CHESS BOARD DETECTION WITH MACHINE LEARNING**



 #   **Project Documentation**

This project aims to:

- Capture a screenshot of a chessboard displayed on the computer screen.
- Find the chess board from the screenshot.
- Crop the chessboard out of the screenshot.
- Split the chessboard into 64 individual squares representing each piece on the board.
- Use a trained image recognition model in Tensorflow to identify the type of piece in each square.

The ultimate goal of the project is to identify the type of piece in each square of a chessboard. This involves a number of steps, including capturing and processing a screenshot of the chessboard, isolating individual squares on the board, and using machine learning to recognize the type of piece in each square.

![Trained model](https://i.imgur.com/1glnIh6.png)

# The program consists of several Python scripts:

**screenshot.py**: Captures a screenshot of the current window displaying the chessboard.   
**crop_the_screenshot.py**: Crops the chessboard out of the screenshot.   
**square_make.py**: Divides the cropped chessboard into 64 squares and saves each square as a separate image file.  
**TF_image_recognition.py**: Trains a convolutional neural network using the images of chess pieces and empty squares to classify the piece in each square.    
**square_test.py**: Loads the trained model and uses it to predict the type of piece in each square.  
**black_to_play.py**: Rotates the board 180 degrees and changes the side to move in the FEN code.  
**main.py**: Contains the main function to run the program.




# Libraries

- ***chess***    
 - ***os***    
- ***tkinter***   
- ***webbrowser***   
- ***sys***   
- ***Stockfish***  
- ***datetime***  
- ***opencv-python***  
- ***numpy***  
- ***Pillow***  
- ***subprocess***  
- ***ttk***  
- ***tensorflow*** 
- ***matplotlib***      

# Usage

To run the program, run the ```main.py``` script. A GUI window will appear with two buttons: "**Take a Screenshot**" and "**Load FEN**".
Another option is to run the ```main.exe``` file.

![Main Window](https://i.imgur.com/Hg6Drog.png)


**Take a Screenshot**   
Clicking the "**Take a Screenshot**" button will capture a screenshot of the current window displaying the chessboard, crop the chessboard out of the screenshot, split it into 64 individual squares representing each piece on the board, and finally use image recognition to identify the type of piece in each square.

**Load FEN**  
Clicking the "**Load FEN**" button will prompt the user to enter a valid Forsyth-Edwards Notation (FEN) string. The program will then display the board with the pieces positioned according to the FEN string.

![Screenshot taken or FEN Loaded](https://i.imgur.com/L8xTX0k.png)

**Evaluation**

Evaluation button: When you click on the "Evaluation" button, the program will call the get_evaluation() method from the Stockfish engine to calculate the evaluation score of the current board state. The evaluation score is a numerical value that represents how advantageous the current position is for the player whose turn it is to move. The evaluation score will be displayed on the GUI in a label next to the button.

**Best Move**

Best move button: When you click on the "**Best move**" button, the program will call the get_best_move() method from the Stockfish engine to calculate the best move to make, based on the current board state. The best move will be displayed on the GUI in a label next to the button.

**Editor** 

The "**Editor**" button takes the current FEN position of the chess board and opens it in the lichess.org's chessboard editor. Users can then use this editor to make moves and experiment with different positions and setups.

**Analysis**

The "**Analysis**" button takes the current FEN position of the chess board and opens it in the lichess.org's game analysis page. Users can then analyze the position with the built-in chess engine and explore possible moves and variations.

![Lichess Board Editor](https://i.imgur.com/NpUjHBS.png)

**FEN History** 

FEN History button: When you click on the "**FEN History**" button, the program will open a new window that displays a list of FEN strings representing the board state at different points in the game. These FEN strings are stored in a text file named "fen_history.txt".

![FEN History](https://i.imgur.com/Z3ebWHE.png)
