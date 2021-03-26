import tkinter as tk
import time

def board_position_to_xy(position):
    '''
    Takes a string representing a square on the board and returns
    a tuple of the xy coordinates corresponding to the center of the square
    at that board position.
    Board squares are numbered left to right, top to bottom starting at 0,0.

    board_position_to_xy(0, 0)
    >>>(75, 75)
    '''
    x = (int(position[0]) + 0.5) * square_edge_len + width_buffer
    y = (int(position[1]) + 0.5) * square_edge_len + height_buffer

    return (x, y)


def piece_color(piece_position):
    '''
    Takes position and returns fill color of piece at that location.
    '''
    return canvas.itemcget(board[piece_position], "fill")


def select(piece_position):
    '''
    Takes a  position, changes color to indicate selection
    and updates the selection variable to that piece
    '''
    global selected_piece
    selected_piece = piece_position
    #print("Selected piece: " + selected_piece)
    canvas.itemconfig(board[selected_piece], fill=selected_piece_color)
    
def deselect(piece_position):
    '''
    Takes a piece object, returns color to original piece color
    and updates the selection variable to empty
    '''
    global selected_piece
    #print("Selected piece to be deselected: " + piece_position)
    canvas.itemconfig(board[piece_position], fill=black_piece_color)
    selected_piece = ""

def xy_to_board_position(x, y):
    '''
    Takes an x and y coordinate and returns cooresponding
    position on the board in string 'xy' format

    xy_to_board_position(75, 75)
    >>>"00"
    '''
    horizontal_square_pos = (x - width_buffer) // square_edge_len
    vertical_square_pos = (y - height_buffer) // square_edge_len

    return str(horizontal_square_pos) + str(vertical_square_pos)


def create_piece(position, fill_color):
    '''
    Takes a board position and returns a piece object which is
    created and drawn at the center of starting_square.
    '''

    (x, y) = board_position_to_xy(position)

    gamepiece = canvas.create_oval(
    x - checker_dia // 2,
    y - checker_dia // 2,
    x + checker_dia // 2,
    y + checker_dia // 2,
    fill = fill_color
    )
    return gamepiece



def move_piece(piece_position, target_position):
    '''
    Takes a reference to an oval object (gamepiece) and coordinates.
    Moves gamepiece to center of destination square.
    '''
    global board

    # Relative position of click within square
    #x_rel = (x - width_buffer) % square_edge_len
    #y_rel = (y - height_buffer) % square_edge_len

    # Center of clicked square
    #x = x - x_rel + square_edge_len // 2
    #y = y - y_rel + square_edge_len // 2

    # Get destination coordinates and piece object to move
    (x, y) = board_position_to_xy(target_position)
    #print("x y coords are " + str(x) + " " + str(y))
    piece = board[piece_position]

    # Move gamepiece to square
    canvas.coords(
        piece,
        x - checker_dia // 2,
        y - checker_dia // 2,
        x + checker_dia // 2,
        y + checker_dia // 2)

    # Update piece location in board dict
    #print("Piece moved to " + target_position)
    board[piece_position] = ""
    #print("piece is now: " + str(piece))
    board[target_position] = piece
    #print("piece is now: " + str(piece))
    canvas.tag_raise(piece)

def valid_move(piece_position, target_position):
    '''
    Returns true if the attempted move is valid
    '''
    (piece_x, piece_y) = (int(piece_position[0]), int(piece_position[1]))
    (target_x, target_y) = (int(target_position[0]), int(target_position[1]))


    # Moves must be within bounds
    if not (target_y < squares_per_row and target_y >= 0):
        #print("tried to move out of bounds vertically")
        #print("target_y is " + str(target_y))
        return False
    elif not (target_x < squares_per_row and target_x >= 0):
        #print("tried to move out of bounds horizontally")
        return False

    # Moves must be to an empty square
    if board[target_position] != "":
        #print("board was empty at target position " + target_position)
        return False

    # Moves must be diagonal
    x_diff = piece_x - target_x

    if piece_color(piece_position) == red_piece_color:
        y_diff = target_y - piece_y
    else:
        y_diff = piece_y - target_y

    #print("x_diff is " + str(x_diff))
    #print("y_diff is " + str(y_diff))

    # target x must be +/- 1, y must be +1 from piece
    if abs(x_diff) == 1 and y_diff == 1:
        validity = True
    # or if jump, two spaces diagonally over opponent piece
    elif abs(x_diff) == 2 and y_diff == 2:
        middle_position = str(x_diff//2) + str(y_diff//2)
        if piece_color(middle_position) != piece_color(piece_position):
            validity = True
        
    else:
        #print("problem with target square's distance from piece")
        return False

    # Note: user moves are kept in bounds by restricting clicks to within board

    return validity

def computer_move():

    #if not user_turn:
    for position in board:
        gamepiece = board[position]
        #print(board)
        #print(gamepiece)
        if gamepiece != "":
            #print("I found a piece to move!")
            if canvas.itemcget(gamepiece, "fill") == red_piece_color:
                #print("and it's red")
                # options to move piece
                x1 = int(position[0]) + 1
                x2 = int(position[0]) - 1
                y = int(position[1]) + 1

                target1 = str(x1) + str(y)
                target2 = str(x2) + str(y)
                
                if valid_move(position, target1):
                    #print("computer moving piece " + position + " to " + target1)
                    move_piece(position, target1)
                    global user_turn
                    user_turn = True
                    return
                #if valid_move
                # move option 2

    

def click(event):

    global selected_piece
    global board

    # Determine which square was clicked
    clicked_position = xy_to_board_position(event.x, event.y)
    horizontal_position = int(clicked_position[0])
    vertical_position = int(clicked_position[1])

    # Ignore clicking outside the board
    if horizontal_position < 0 or horizontal_position >= squares_per_row:
        return
    elif vertical_position < 0 or vertical_position >= squares_per_row:
        return
    
    # Get rectangle object of square
    clicked_square = squares[clicked_position]
    
    # Case 1: A piece is selected and is clicked again
    # Deselect that piece
    if selected_piece and selected_piece == clicked_position:
        deselect(selected_piece)
    # Case 2: no piece selected and black piece clicked
    # Select that piece
    elif not selected_piece and board[clicked_position] != "":
        if piece_color(clicked_position) == black_piece_color:
                select(clicked_position)
    # Case 3: piece already selected and black square clicked
    # Move the piece
    elif selected_piece and canvas.itemcget(clicked_square, "fill") == "black":
        if valid_move(selected_piece, clicked_position):
            move_piece(selected_piece, clicked_position) # set new piece position
            deselect(clicked_position)
            #time.sleep(1)

            # Computer's turn!
            #print("it's my turn!")
            computer_move()


# -------- VARIABLES ---------------
# Board
square_edge_len = 50
checker_dia = 40
squares_per_row = 8
selected_piece = ""
black_piece_color = "grey"
red_piece_color = "tomato"
selected_piece_color = "white"

# Window
width_buffer = 50
height_buffer = 100
window_width = (square_edge_len*squares_per_row)+(2*width_buffer)
window_height = (square_edge_len*squares_per_row)+(2*height_buffer)

user_turn = True

# --------- MAIN SCRIPT --------------
# create window
window = tk.Tk()
window.geometry(str(window_width) +"x"+ str(window_height))
window.title("Jon's Amateur Checkers")

# create canvas
canvas = tk.Canvas(
    master=window,
    width=600,
    height=500,
    relief="raised",
    )

# CREATE BOARD
red = True  # flag for square color
squares = {}  # dict to store square objects
board = {}  # dict to store piece locations

for i in range(squares_per_row):
    for j in range(squares_per_row):
        
        position = str(j) + str(i)
        
        # determine square color
        if red:
            square_color = "red"
        else:
            square_color = "black"

        # create and store square in dict (squares[x_pos_str + y_pos_str])
        squares[position] = canvas.create_rectangle(
            width_buffer + j*square_edge_len,
            height_buffer + i*square_edge_len,
            width_buffer + (j+1)*square_edge_len,
            height_buffer + (i+1)*square_edge_len,
            fill=square_color,
            outline = "yellow"
            )

        # draw and store board and pieces
        if square_color == "black" and i >= (squares_per_row - 3):
            board[position] = create_piece(position, black_piece_color)
        elif square_color == "black" and i < 3:
            board[position] = create_piece(position, red_piece_color)
        else:
            board[position] = ""

        # invert square color for next iterationu
        # skip last square to get alternating pattern
        if j < (squares_per_row-1):
            red = not red


canvas.bind("<Button-1>", click)

# pack it up
canvas.pack()

# trying something
#window.after(


# main loop with listeners, etc
window.mainloop()



