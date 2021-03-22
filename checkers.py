import tkinter as tk


def gamepiece_click(event):

    x = event.x
    y = event.y

    # Determine which square was clicked
    horizontal_square_pos = (x - width_buffer) // square_edge_len
    vertical_square_pos = (y - height_buffer) // square_edge_len

    # change clicked square color
    #clicked_square = squares[str(horizontal_square_pos) + str(vertical_square_pos)]
    #canvas.itemconfig(gamepiece, fill="blue")

    # Move gamepiece to click position
    canvas.coords(gamepiece, x - checker_dia // 2, y - checker_dia // 2, x + checker_dia // 2, y + checker_dia // 2)

    
    

    #if (event.x > 0 and event.x < 50) and (event.y > 0 and event.y < 50):
    #    canvas.itemconfig(gamepiece, fill="white")

# -------- VARIABLES ---------------
# Board
square_edge_len = 50
checker_dia = 40
squares_per_row = 8

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
squares = {}  # dict to store squares

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

        # invert square color for next iteration
        # skip last square to get alternating pattern
        if j < (squares_per_row-1):
            red = not red

# draw pieces
gamepiece = canvas.create_oval(
    width_buffer+10,
    height_buffer+10,
    width_buffer + checker_dia,
    height_buffer + checker_dia,
    fill = 'grey'
    )

canvas.bind("<Button-1>", gamepiece_click)

# pack it up
canvas.pack()



# main loop with listeners, etc
window.mainloop()



# add text
#greeting = tk.Label(text = "Hello World!")
#greeting.pack()

# add button
#button = tk.Button(master=window, text="Click Me", command=click_test)
#button.pack()

# add oval to canvas
#oval = canvas.create_oval(10, 10, 40, 40)
