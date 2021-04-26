import tkinter as tk
import time



'''

Next steps:
X Make piece_color() into a piece_type() function that returns either red checker,
  black checker, red king or black king.
X Set behavior so that kings can move in any direction
X Figure out why black pieces can move backwards even if they are not kings
- Computer should be able to move king if they have one (or several)

'''


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


def piece_type(piece_position):
    '''
    Takes a position and returns the type of the piece at that location,
    either "black_piece", "red_piece", "black_king", "red_king".

    piece_type("00")
    >>>"red_king"
    '''

    # Get color information from piece
    fill = canvas.itemcget(board[piece_position], "fill")
    outline = canvas.itemcget(board[piece_position], "outline")

    # Outline color determines king or checker
    if outline == "black":
        status = "checker"
    else:
        status = "king"

    # Fill color determines red or black piece
    if fill == black_piece_color or fill == selected_piece_color:
        color = "black"
    else:
        color = "red"
        
    return color + "_" + status


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
    fill = fill_color,
    )

    return gamepiece

def make_king(position):
    '''
    Takes a board position containing a piece
    turns that piece into a king by adding a border around the piece
    '''
    piece = board[position]

    # Add border (outline) to piece
    if canvas.itemcget(piece, "fill") == black_piece_color:
        canvas.itemconfig(piece, outline=black_king_color)
    else:
        canvas.itemconfig(piece, outline=red_king_color)

    # Thicken border
    canvas.itemconfig(piece, width=border_thickness)


def remove_piece(position):
    canvas.delete(board[position])
    board[position] = ""


def move_piece(piece_position, target_position):
    '''
    Takes a reference to an oval object (gamepiece) and coordinates.
    Moves gamepiece to center of destination square.
    '''
    global board
    global window

    # Get destination and piece to move
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
    board[piece_position] = ""
    board[target_position] = piece
    canvas.tag_raise(piece)

def jump(position, target_position):
    jumped_x = (int(position[0]) + int(target_position[0])) // 2
    jumped_y = (int(position[1]) + int(target_position[1])) // 2
    jumped_position = str(jumped_x) + str(jumped_y)
    move_piece(position, target_position)
    remove_piece(jumped_position)

def valid_move(piece_position, target_position):
    '''
    Returns true if the attempted move is valid
    '''

    # Assume false
    validity = False

    # Target position may not be negative
    if '-' in target_position:
        return False
    else:
        (piece_x, piece_y) = (int(piece_position[0]), int(piece_position[1]))
        (target_x, target_y) = (int(target_position[0]), int(target_position[1]))
 
    # Target must be on the board
    if not (target_y < squares_per_row):
        return False
    elif not (target_x < squares_per_row):
        return False

    # Target must be an empty square
    if board[target_position] != "":
        return False

    # Target must be diagonal from selected piece
    x_diff = abs(piece_x - target_x)

    # Account for allowable y directions in different cases
    if piece_type(piece_position) == "red_checker":
        y_diff = target_y - piece_y
    elif piece_type(piece_position) == "black_checker":
        y_diff = piece_y - target_y
    else: # piece is a king
        y_diff = abs(piece_y - target_y)

    # target x must be +/- 1, y must be +1 from piece
    if x_diff == 1 and y_diff == 1:
        validity = True
    # if jump, must be two spaces diagonally over opponent piece
    elif x_diff == 2 and y_diff == 2:
        middle_position = str((piece_x + target_x)//2) + str((piece_y + target_y)//2)
        if board[middle_position] != "":
            if piece_color(middle_position) == piece_color(piece_position) and piece_color(piece_position) == red_piece_color:
                return False
            elif selected_piece and piece_color(middle_position) == black_piece_color:  
                return False
            else:
                validity = True
    else:
        return False

    return validity

def computer_move():
    # Check for jumps first, then single moves
    for offset in [2, -2, 1, -1]:
        for position in board:
            gamepiece = board[position]
            if gamepiece != "":
                if canvas.itemcget(gamepiece, "fill") == red_piece_color:
                    # options to move piece

                    x = int(position[0])
                    y = int(position[1])
                    
                    target_x = x + offset
                    target_y = y + abs(offset)

                    # Check for valid move
                    target_position = str(target_x) + str(target_y)
                    if valid_move(position, target_position):
                        if abs(offset) == 2:
                            jump(position, target_position)
                        else:
                            move_piece(position, target_position)
                        # Does computer get a king? 
                        if int(target_position[1]) == squares_per_row - 1:
                            make_king(target_position)
                        return
                            
            
## ----------------- MAIN FUNCTION --------------------------------------------

def click(event):

    global selected_piece
    global board

    # Get location of clicked square
    clicked_position = xy_to_board_position(event.x, event.y)
    horizontal_position = int(clicked_position[0])
    vertical_position = int(clicked_position[1])

    # If click is not on the game board, do nothing
    if horizontal_position < 0 or horizontal_position >= squares_per_row:
        return
    elif vertical_position < 0 or vertical_position >= squares_per_row:
        return
    
    # Get rectangle object of square
    clicked_square = squares[clicked_position]
    
    ## CASE 1: DESELECT
    #  A black piece is clicked but was already selected
    if selected_piece and selected_piece == clicked_position:

        deselect(selected_piece)
        
    ## CASE 2: SELECT
    #  A black piece is clicked, was not already selected
    elif not selected_piece and board[clicked_position] != "":
        if piece_color(clicked_position) == black_piece_color:

            select(clicked_position)
                
    ## CASE 3: MOVE
    #  A black square is clicked, piece was already selected, and move is valid
    elif selected_piece and canvas.itemcget(clicked_square, "fill") == "black":
        if valid_move(selected_piece, clicked_position):

            # Jump or move depending on distance between selected piece and clicked square
            if abs(int(selected_piece[0]) - int(clicked_position[0])) == 2:
                jump(selected_piece, clicked_position)
            else:
                move_piece(selected_piece, clicked_position)

            # The selected piece is now at the clicked position and is deselected
            deselect(clicked_position)

            # If pieces made it to the other side, king me!
            if piece_color(clicked_position) == black_piece_color and clicked_position[1] == "0":
                make_king(clicked_position)

            # Delay before computer moves
            window.update()
            window.after(1500)

            # Computer's turn!
            computer_move()


# -------- VARIABLES ---------------
# Board/Piece Dimensions
square_edge_len = 50
checker_dia = 40
border_thickness = 5
diagonal_len = round((2*square_edge_len)**0.5)
squares_per_row = 8

# Board/Piece States
selected_piece = ""
red = True  # flag for square color

squares = {}  # dict to store square objects

board = {}  # Keys are two-integer strings representing board position
            # ie "00" is the top leftmost square.
            # Value is a piece object if there is a piece on that square
            # If no piece is present, the value will be set to ""

user_turn = True

# Colors
black_piece_color = "grey"
red_piece_color = "tomato"
black_king_color = "yellow"
red_king_color = "white"
selected_piece_color = "white"

# Window Dimensions
width_buffer = 50
height_buffer = 100
window_width = (square_edge_len*squares_per_row)+(2*width_buffer)
window_height = (square_edge_len*squares_per_row)+(2*height_buffer)

user_turn = True

# --------- INITIALIZE GAME --------------
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

# main loop with listeners, etc
window.mainloop()