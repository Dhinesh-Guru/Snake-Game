from tkinter import *
import random

#Some constants for the game
GAME_WIDTH=800        #Feel free to change the width and height of the game window
GAME_HEIGHT=600
SPEED=100   #lower the number faster the game
SPACE_SIZE=50   #Size of items such as food body parts
BODY_PARTS=3    #Body parts of snake at the starting of game
SNAKE_COLOUR="#00FF00"
FOOD_COLOUR="#FF0000"
BACKGROUND_COLOUR="#000000"


class Snake:
    def __init__(self):
        self.body_size=BODY_PARTS
        self.coordinates=[]
        self.squares=[]

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0,0])   #body part at start of game

        for x,y in self.coordinates:
            square=canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOUR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x=random.randint(0,int(GAME_WIDTH/SPACE_SIZE)-1)*SPACE_SIZE
        y=random.randint(0,int(GAME_HEIGHT/SPACE_SIZE)-1)*SPACE_SIZE
        self.coordinates=[x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOUR,tag="food")

def next_turn(snake,food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    
    snake.coordinates.insert(0, (x, y))
    square=canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOUR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score+=1
        label.config(text="Score: {}".format(score))
        canvas.delete("food")   #delete the food object from canvas using the tag
        food=Food()
    else:   #delete the previous squares if the snake don't eat any food
        del snake.coordinates[-1]  
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    
    if check_collisions(snake):
        game_over()
    else:
         window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    
    if new_direction == "left":
        if direction != "right":
            direction = new_direction
    elif new_direction == "right":
        if direction != "left":
            direction = new_direction
    elif new_direction == "up":
        if direction != "down":
            direction = new_direction
    elif new_direction == "down":
        if direction != "up":
            direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH:   #To check if the snake collide with sides
        return True
    elif y < 0 or y >= GAME_HEIGHT: #To check if the snake collide with top/bottom
        return True

    for body_part in snake.coordinates[1:]:  #To check if the snake collide with itself
        if x == body_part[0] and y == body_part[1]:
            return True
    
    return False

def game_over():
    global replay_button, exit_btn
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2,canvas.winfo_height()/3,
                        font=("Perpetua Titling MT",60,"bold"),text="GAME OVER",fill="red",tag="gameover")
    #Replay button
    replay_button=Button(window,text="Replay",font=('consolas',20),bg="#00FF00",
                            fg="white",command=restart_game)
    replay_btn_window = canvas.create_window(canvas.winfo_width()/2, 
                                            canvas.winfo_height()/2,
                                            window=replay_button)
    # Exit button
    exit_btn = Button(window, text="Exit", font=("consolas", 20), bg="red", fg="white",
                      command=window.destroy)
    exit_btn_window = canvas.create_window(canvas.winfo_width()/2, canvas.winfo_height()/2 + 70,
                                           window=exit_btn)

def restart_game():
    global snake,food,score,direction
    replay_button.destroy()
    exit_btn.destroy()
    canvas.delete(ALL)
    score=0
    direction="down"
    label.config(text="Score: {}".format(score))
    
    snake=Snake()
    food=Food()
    next_turn(snake,food)

window=Tk()
window.title("Snake Game")
window.iconphoto(True,PhotoImage(file="Snake Game/snake-icon.png"))
window.resizable(False,False)   #Prevent the window resizing
score=0
direction='down'

label=Label(window,text="Score: {}".format(score),font=('consolas',30))
label.pack()

canvas=Canvas(window,bg=BACKGROUND_COLOUR,height=GAME_HEIGHT,width=GAME_WIDTH)
canvas.pack()

window.update()
#To make the game window open close to the center
window_width=window.winfo_width()
window_height=window.winfo_height()
screen_width=window.winfo_screenwidth()
screen_height=window.winfo_screenheight()

x=int((screen_width/2)-(window_width/2))
y=int((screen_height/2)-(window_height/2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>',lambda event: change_direction('left'))
window.bind('<Right>',lambda event: change_direction('right'))
window.bind('<Up>',lambda event: change_direction('up'))
window.bind('<Down>',lambda event: change_direction('down'))

snake=Snake()
food=Food()
next_turn(snake,food)

window.mainloop()