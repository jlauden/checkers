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


def create_piece(horizontal_pos, vertical_pos):
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
    fill = 'grey'
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
        canvas.itemconfig(board[selected_piece], fill="grey")
        selected_piece = ""
    # Case 2: no piece selected and piece clicked
    # Select that piece
    elif not selected_piece and board[clicked_position] != "":
        selected_piece = clicked_position
        canvas.itemconfig(board[selected_piece], fill="white")
    # Case 3: piece already selected and black square clicked
    # Move the piece
    elif selected_piece and canvas.itemcget(clicked_square, "fill") == "black":
        move_piece(board[selected_piece], x, y) # set new piece position
        canvas.itemconfig(board[selected_piece], fill="grey")
        board[selected_piece] = "" # clear last piece position
        selected_piece = ""

# -------- VARIABLES ---------------
# Board
square_edge_len = 50
checker_dia = 40
squares_per_row = 8
selected_piece = "" 

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

        # draw and store pieces
        if square_color == "black" and i >= (squares_per_row - 3):
            board[str(j)+str(i)] = create_piece(j, i)
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



