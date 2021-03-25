import tkinter as tk


def board_position_to_xy(horizontal_pos, vertical_pos):
    '''
    Takes two integers representing a square on the board and returns
    a tuple of the xy coordinates corresponding to the center of the square
    at that board position.
    Board squares are numbered left to right, top to bottom starting at 0,0.

    board_position_to_xy(0, 0)
    >>>(75, 75)
    '''
    x = (int(horizontal_pos) + 0.5) * square_edge_len + width_buffer
    y = (int(vertical_pos) + 0.5) * square_edge_len + height_buffer
    return (x, y)


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


def create_piece(horizontal_pos, vertical_pos, fill_color):
    '''
    Takes a board position and returns a piece object which is
    created and drawn at the center of starting_square.
    '''

    (x, y) = board_position_to_xy(int(horizontal_pos), int(vertical_pos))

    gamepiece = canvas.create_oval(
    x - checker_dia // 2,
    y - checker_dia // 2,
    x + checker_dia // 2,
    y + checker_dia // 2,
    fill = fill_color
    )
    return gamepiece



def move_piece(piece, x, y):
    '''
    Takes a reference to an oval object (gamepiece) and coordinates.
    Moves gamepiece to center of destination square.
    '''
    global board

    # Relative position of click within square
    x_rel = (x - width_buffer) % square_edge_len
    y_rel = (y - height_buffer) % square_edge_len

    # Center of clicked square
    x = x - x_rel + square_edge_len // 2
    y = y - y_rel + square_edge_len // 2

    # Move gamepiece to square
    canvas.coords(
        piece,
        x - checker_dia // 2,
        y - checker_dia // 2,
        x + checker_dia // 2,
        y + checker_dia // 2)

    board[xy_to_board_position(x, y)] = piece


def valid_move(piece_position, target_position):
    '''
    Returns true if the attempted move is valid
    '''

    x_diff = int(piece_position[0]) - int(target_position[0])
    y_diff = int(piece_position[1]) - int(target_position[1])

    # target x must be +/- 1, y must be +1 from piece
    if abs(x_diff) == 1 and y_diff == 1:
        return True
    else:
        return False
    

def click(event):

    x = event.x
    y = event.y
    global selected_piece
    global board

    # Determine which square was clicked
    horizontal_square_pos = (x - width_buffer) // square_edge_len
    vertical_square_pos = (y - height_buffer) // square_edge_len
    clicked_position = str(horizontal_square_pos) + str(vertical_square_pos)

    # Get rectangle object of square
    clicked_square = squares[clicked_position]

    
    # Case 1: selected piece is clicked again
    # Deselect that piece
    if selected_piece and selected_piece == clicked_position:
        canvas.itemconfig(board[selected_piece], fill=black_piece_color)
        selected_piece = ""
    # Case 2: no piece selected and black piece clicked
    # Select that piece
    elif not selected_piece and board[clicked_position] != "":
        if canvas.itemcget(board[clicked_position], "fill") == black_piece_color:
                selected_piece = clicked_position
                canvas.itemconfig(board[selected_piece], fill=selected_piece_color)
    # Case 3: piece already selected and black square clicked
    # Move the piece
    elif (selected_piece and canvas.itemcget(clicked_square, "fill") == "black") and board[clicked_position] == "":
        if valid_move(selected_piece, clicked_position):
            move_piece(board[selected_piece], x, y) # set new piece position
            canvas.itemconfig(board[selected_piece], fill=black_piece_color)
            board[selected_piece] = "" # clear last piece position
            selected_piece = ""


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

        # determine square color
        if red:
            square_color = "red"
        else:
            square_color = "black"

        # create and store square in dict (squares[x_pos_str + y_pos_str])
        squares[str(j)+str(i)] = canvas.create_rectangle(
            
            width_buffer + j*square_edge_len,
            height_buffer + i*square_edge_len,
            width_buffer + (j+1)*square_edge_len,
            height_buffer + (i+1)*square_edge_len,
            fill=square_color,

            outline = "yellow"
            )

        # draw and store board and pieces
        if square_color == "black" and i >= (squares_per_row - 3):
            board[str(j)+str(i)] = create_piece(j, i, black_piece_color)
        elif square_color == "black" and i < 3:
            board[str(j)+str(i)] = create_piece(j, i, red_piece_color)
        else:
            board[str(j)+str(i)] = ""

        # invert square color for next iteration
        # skip last square to get alternating pattern
        if j < (squares_per_row-1):
            red = not red


canvas.bind("<Button-1>", click)

# pack it up
canvas.pack()



# main loop with listeners, etc
window.mainloop()



