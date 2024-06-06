from tkinter import *
from random import randint
import pygame
from pygame.locals import *

# Create the menu window
menu_window = Tk()

# Set the title of the menu window
menu_window.title("Snake Game Menu")

# Create the canvas
canvas = Canvas(menu_window, width=500, height=450, background="black")
photo = PhotoImage(file="Snake_logo.png")
canvas.create_image(0, 0, anchor=NW, image=photo)
# Place the canvas
canvas.pack()

# Create the menu buttons
Button(menu_window, text="Play", fg="yellow", bg="grey", command=menu_window.destroy, relief=FLAT).pack(side=TOP,padx=10,pady=10)


# The menu window loop will stop when the red cross is clicked
menu_window.mainloop()

# Create display surface
#menu_window = pygame.display.set_mode((300, 300))
pass
# Initialize the mixer module
pygame.mixer.init()

# Create a window using the Tk() function
window = Tk()

# Change the title of the window
window.title('The Snake')

# Get screen dimensions
screen_height = window.winfo_screenheight()
screen_width = window.winfo_screenwidth()

# Convert height (H) and width (L) data to int, then to string,
# and adjust the desired dimensions
H = str(int(screen_height / 1.1))
L = str(int(screen_width / 2))

# Apply the desired size to the window using the geometry(wxh+X+Y) function where:
# w, h are respectively the width and the height
# X and Y are the coordinates of the origin point relative to the top-left corner of the window
# the x and the two + are separators
# to insert variables, we concatenate them with strings using the concatenation operator +
window.geometry(L + "x" + H + "+0+0")

# Define the dimensions of the game board
board_width = screen_width / 2
board_height = screen_height / 1.2

# Create a Canvas for the game board
board = Canvas(window, width=board_width, height=board_height, bg="pink")
# "side" specifies where the canvas begins
board.pack(side="bottom")

# Create a Canvas for the score
score_bar = Text(window, width=int(screen_width / 2), height=int(board_height / 10), bg="light blue")
# Place the score bar
score_bar.pack(side="top")
# Write the initial score in the score bar
score_bar.insert(END, "score: 0\n")

# Define the number of squares on the board
num_squares = 75

# Define the dimensions of a square
square_width = (board_width / num_squares)
square_height = (board_height / num_squares)


# Function to determine the size of the squares on the board and color them green to symbolize the snake
def fill_square(x, y, color="green"):
    # Define the coordinates (origin_squareX1; origin_squareY1) of the top-left point of the square
    # and (origin_squareX2; origin_squareY2) of the bottom-right point of the square
    origin_squareX1 = x * square_width
    origin_squareY1 = y * square_height
    origin_squareX2 = origin_squareX1 + square_width
    origin_squareY2 = origin_squareY1 + square_height

    # Fill the rectangle
    board.create_rectangle(origin_squareX1, origin_squareY1, origin_squareX2, origin_squareY2, fill=color)


# Return a random square
def random_square():
    randomX = randint(0, num_squares - 1)
    randomY = randint(0, num_squares - 1)

    return (randomX, randomY)


# Draw the snake, the argument being the list snake
def draw_snake(snake):
    # As long as there are squares in snake
    for square in snake:
        # Get the coordinates of the square
        x, y = square
        # Color the square
        fill_square(x, y)


# Return 1 if the square is in the snake, 0 otherwise
def is_in_snake(square):
    if square in SNAKE:
        return 1
    else:
        return 0


# Return 1 if the square is an obstacle, 0 otherwise
def is_in_obstacle(square):
    if square in OBSTACLES:
        return 1
    else:
        return 0


# Return a random fruit that is not in the snake or in the obstacles
def random_fruit():
    # Choose a random fruit
    fruit = random_square()

    # While the random fruit is in the snake or in the obstacles
    while is_in_snake(fruit) or is_in_obstacle(fruit):
        # Choose a new random fruit
        fruit = random_square()

    return fruit


# Draw the fruit, same as coloring a square, but use create_oval instead
def draw_fruit():
    global FRUIT

    x, y = FRUIT

    origin_squareX1 = x * square_width
    origin_squareY1 = y * square_height
    origin_squareX2 = origin_squareX1 + square_width
    origin_squareY2 = origin_squareY1 + square_height

    # Fill the oval in red for the fruit
    board.create_oval(origin_squareX1, origin_squareY1, origin_squareX2, origin_squareY2, fill="red")


# Draw the obstacles
def draw_obstacles():
    for obstacle in OBSTACLES:
        x, y = obstacle
        fill_square(x, y, "brown")


# These four functions allow movement in four directions of the snake
# they update the coordinates of the movement
def left_key(event):
    global MOVEMENT
    MOVEMENT = (-1, 0)


def right_key(event):
    global MOVEMENT
    MOVEMENT = (1, 0)


def up_key(event):
    global MOVEMENT
    MOVEMENT = (0, -1)


def down_key(event):
    global MOVEMENT
    MOVEMENT = (0, 1)


# Specify the functions to call after pressing the arrow keys (only works if the window has focus)
window.bind("<Left>", left_key)
window.bind("<Right>", right_key)
window.bind("<Up>", up_key)
window.bind("<Down>", down_key)


# Update the DEAD variable indicating if the player has lost
def snake_dead(new_head):
    global DEAD

    new_head_x, new_head_y = new_head

    # If the snake eats itself (except at the start, i.e.: except when MOVEMENT equals (0, 0))
    # OR if it goes out of the canvas
    if (is_in_snake(new_head) and MOVEMENT != (0, 0)) or new_head_x < 0 or new_head_y < 0 or new_head_x >= num_squares or new_head_y >= num_squares or is_in_obstacle(new_head):
        # Then, the player has lost
        DEAD = 1


# Update the score
def update_score():
    global SCORE, SPEED

    SCORE += 1
    score_bar.delete(0.0, 3.0)
    score_bar.insert(END, "score: " + str(SCORE) + "\n")

    # Increase speed every 5 points
    if SCORE % 5 == 0:
        SPEED = max(10, SPEED - 5)


# Update the snake
def update_snake():
    global SNAKE, FRUIT

    # Get the coordinates of the current head
    (old_head_x, old_head_y) = SNAKE[0]
    # Get the movement values
    movement_x, movement_y = MOVEMENT
    # Calculate the coordinates of the new head
    new_head = (old_head_x + movement_x, old_head_y + movement_y)
    # Check if the player has lost
    snake_dead(new_head)
    # Add the new head
    SNAKE.insert(0, new_head)

    # If the snake eats a fruit
    if new_head == FRUIT:
        # Generate a new fruit
        FRUIT = random_fruit()
        # Update the score
        update_score()
    # Otherwise
    else:
        # Remove the last element of the snake (i.e.: do not grow)
        SNAKE.pop()


# Reset the variables for a new game
def reset_game():
    global SNAKE, FRUIT, MOVEMENT, SCORE, DEAD, SPEED

    # Initial snake
    SNAKE = [random_square()]
    # Initial fruit
    FRUIT = random_fruit()
    # Initial movement
    MOVEMENT = (0, 0)
    # Initial score
    SCORE = 0
    # Initial speed (time interval between updates)
    SPEED = 70
    # Initial lost variable (will be set to 1 if the player loses)
    DEAD = 0


# Main function
def task():
    # Update the display and keyboard events
    window.update()
    window.update_idletasks()
    # Update the snake
    update_snake()
    # Delete all elements from the board
    board.delete("all")
    # Redraw the obstacles
    draw_obstacles()
    # Redraw the fruit
    draw_fruit()
    # Redraw the snake
    draw_snake(SNAKE)

    # If the player has lost
    if DEAD:
        # Clear the score bar
        score_bar.delete(0.0, 3.0)
        # Display that the player lost
        score_bar.insert(END, "Lost with a score of " + str(SCORE))
        # Prepare a new game
        reset_game()
        # Call the main function again
        window.after(1000, task)
    # Otherwise
    else:
        # Call the main function again
        window.after(SPEED, task)


# Initialize the obstacles
OBSTACLES = [random_square() for _ in range(10)]
# Initial snake: a list with a random square
SNAKE = [random_square()]
# Initial fruit
FRUIT = random_fruit()
# Initial movement, a pair of integers representing the movement coordinates, initially not moving
MOVEMENT = (0, 0)
# Initial score
SCORE = 0
# Variable to know if the player has lost, will be set to 1 if the player loses
DEAD = 0
# Initial speed
SPEED = 70

# Call the main function for the first time just after entering the window loop
window.after(0, task())

# Create a loop that will display the window
# as long as the user does not click the red cross in the top right
window.mainloop()
