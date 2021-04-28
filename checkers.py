import tkinter as tk
import time
import random



'''

Next steps:

X Make piece_color() into a piece_type() function that returns either red checker,
  black checker, red king or black king.
X Set behavior so that kings can move in any direction
X Figure out why black pieces can move backwards even if they are not kings
X Debug computer move to figure out why all pieces can get locked up on the right hand side
X Modify array of "offset" in computer_move() to include lower left and upper right
  diagonal moves (currently only looks for upper left and lower right quadrants at distances
  of 2, then 1 away from each piece)
X Randomize which quadrant is picked first while maintaining jumps first over normal moves

- Computer should be able to move king if they have one (or several)

'''


def board_position_to_xy(piece_position):
    '''
    Takes a string representing a position on the board and returns
    a tuple (x, y) of coordinates corresponding to the center of the square
    at that board position.

    board_position_to_xy(0, 0)
    >>>(75, 75)
    '''

    # Calculate coordinates of the center of the square at piece_position
    x = (int(piece_position[0]) + 0.5) * square_edge_len + width_buffer
    y = (int(piece_position[1]) + 0.5) * square_edge_len + height_buffer

    return (x, y)


def piece_color(piece_position):
    '''
    Takes position and returns fill color of piece at that location.

    piece_color("10")
    >>>"tomato"
    '''

    return canvas.itemcget(board[piece_position], "fill")


def piece_type(piece_position):
    '''
    Takes a position and returns the type of the piece at that location,
    either "black_piece", "red_piece", "black_king", "red_king".

    piece_type("10")
    >>>"red_king"
    '''

    # Get color information from piece
    fill = canvas.itemcget(board[piece_position], "fill")
    outline = canvas.itemcget(board[piece_position], "outline")

    # Outline color of piece indicates whether it is a king or a checker
    if outline == "black":
        status = "checker"
    else:
        status = "king"

    # Fill color of piece indicates red/black
    if fill == black_piece_color or fill == selected_piece_color:
        color = "black"
    else:
        color = "red"
        
    return color + "_" + status


def select(piece_position):
    '''
    Takes a string as position, changes color to indicate selection
    and updates the selection variable to that piece.
    '''

    # Update selected_piece variable to new position
    global selected_piece
    selected_piece = piece_position

    # Change piece color to indicate that it is selected
    canvas.itemconfig(board[selected_piece], fill=selected_piece_color)
    

def deselect(piece_position):
    '''
    Takes a position, returns color to original piece color
    and updates the selection variable to empty
    '''
    global selected_piece

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
    Takes a board position, creates and draws a piece at that position
    and returns the piece object that was created.
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
    Takes a board position containing a piece and
    turns that piece into a king by adding a border around the piece.

    make_king("10")
    >>>
    '''

    piece = board[position]

    # Add border (outline) to piece
    if canvas.itemcget(piece, "fill") == black_piece_color:
        canvas.itemconfig(piece, outline=black_king_color)
    else:
        canvas.itemconfig(piece, outline=red_king_color)

    # Set border thickness
    canvas.itemconfig(piece, width=border_thickness)


def remove_piece(piece_position):
    '''
    Takes a position and removes the piece at that position from the board.
    Updates both the board (dict) and the canvas (display).

    remove_piece("45")
    >>>
    '''
    canvas.delete(board[piece_position])
    board[piece_position] = ""


def move_piece(piece_position, target_position):
    '''
    Takes a starting and ending position and moves the piece
    at the starting position to the ending position.
    Updates both the board (dict) and the canvas (display).

    move_piece("34", "45")
    >>>
    '''
    global board
    global window

    # Get destination and piece to move
    (x, y) = board_position_to_xy(target_position)
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


def jump(piece_position, target_position):
    '''
    Takes current position of a piece and a target position representing a jump move.
    Moves the piece from it's current position to the target position and removes the
    piece which was jumped.

    jump("45", "23")
    >>>
    '''

    # Calculate position of jumped piece
    jumped_x = (int(piece_position[0]) + int(target_position[0])) // 2
    jumped_y = (int(piece_position[1]) + int(target_position[1])) // 2
    jumped_position = str(jumped_x) + str(jumped_y)

    move_piece(piece_position, target_position)

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

    # X change may be positive or negative
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
    '''
    Evaluates the board for possible moves the computer can make, then moves a piece
    to complete the computer's turn.  Jumps are prioritized over other moves.
    '''

    # Flag to ensure a move was made
    move_made = False
    
    # The possible changes in position for a given piece if moving or jumping
    jump_offset_list = [[2, 2], [2, -2], [-2, 2], [-2, -2]] 
    move_offset_list = [[1, 1], [1, -1], [-1, 1], [-1, -1]]

    # Randomize order in which moves are attempted
    random.shuffle(jump_offset_list)
    random.shuffle(move_offset_list)

    # Full list of moves to attempt beginning with jumps, then normal moves
    
    jump_offset_list.extend(move_offset_list)
    offset_list = jump_offset_list

    # Generate list representing board positions and randomize its order
    randomized_positions = list(board.keys())
    random.shuffle(randomized_positions)

    # Having this as the outermost loop ensures that no opportunity for a jump will be missed
    for offset in offset_list:
        
        for position in randomized_positions:

            # position must not be empty
            if board[position] != "":
                gamepiece = board[position]

                gamepiece_type = piece_type(position)

                # piece at position must be red checker or king
                if "red" in gamepiece_type:

                    # get x and y parts of piece position
                    x = int(position[0])
                    y = int(position[1])
                    
                    # get x and y parts of target position
                    target_x = x + offset[0]
                    target_y = y + offset[1]

                    # Check for valid move from piece position to target position
                    target_position = str(target_x) + str(target_y)

                    if valid_move(position, target_position):
                        if abs(offset[0]) == 2:
                            jump(position, target_position)
                            move_made = True
                        else:
                            move_piece(position, target_position)
                            move_made = True

                        # Computer gets a king if it makes it to the other side! 
                        if int(target_position[1]) == (squares_per_row - 1) and not gamepiece_type == "red_king":
                            make_king(target_position)

                        # Move has been made, exit function
                        return
    
    # If no moves were made out of all pieces, I deserve an explanation.
    if not move_made:
        print("It appears the computer is out of moves.  You have won!  (Or something went wrong...)")

                            
            
## ----------------- MAIN FUNCTION --------------------------------------------

def click(event):

    global selected_piece
    global board

    # Get location of clicked square
    clicked_position = xy_to_board_position(event.x, event.y)
    horizontal_position = int(clicked_position[0])
    vertical_position = int(clicked_position[1])

    # If click is not on the game board, proceed no further!
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