import turtle
import time
import random
import json

# Move the snake in desired direction.
def move():
    if head.direction == "up":
        y = head.ycor()                 # Y co-ordinate of the snake.
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "right":
        x = head.xcor()                  # X co-ordinate of the snake.
        head.setx(x + 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

def go_up():
    # the snake can't go up from down directly.
    if head.direction != "down":
        head.direction = "up"

def go_down():
    # the snake can't go down from up directly.
    if head.direction != "up":
        head.direction = "down"

def go_right():
    # the snake can't go right from left directly.
    if head.direction != "left":
        head.direction = "right"

def go_left():
    if head.direction != "right":
        head.direction = "left"

# Load the Past game high score in the game.
def load_past_high_score():
    filename = "score.json"
    with open(filename) as file:
        raw_score = json.load(file)

    return raw_score

# Save the updated high score at the end of the game.
def save_current_high_score():
    filename = "score.json"
    with open(filename, 'w') as file:
        json.dump(high_score, file, indent=4)

# Set up the turtle Screen.
win = turtle.Screen()
win.title("The Snake Game")
win.bgcolor("#16161a")
win.setup(600, 600)
win.tracer(0)

# Create the snake head
head = turtle.Turtle()
head.speed(0)
head.shape("circle")
head.shapesize(1.2, 1.2, 2)
head.color('white', '#7f5af0')
head.penup()
head.goto(0, 100)
head.right(90)
head.direction = "stop"

win.listen()
win.onkeypress(go_up, "w")
win.onkeypress(go_down, "s")
win.onkeypress(go_right, "d")
win.onkeypress(go_left, "a")

# Snake's food (Laddu)
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.shapesize(0.6, 0.6)
food.color("#e53170")
food.penup()
food.goto(0, 0)

# score board
score = 0
high_score = load_past_high_score()
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0,277)
pen.write(f"Score: {score} \t\t\t HighScore: {high_score}", font=("Verdana", 15, "normal"), align="center")

segments = []               # List to keep the segment(snake's body) number.    
delay = 0.1                   # Delay the process for the defined time.
# Main game loop
while True:
    win.update()
    move()
    time.sleep(delay)

    
    if head.distance(food) < 15:
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)

        # Increase the score.
        score += 10
        if score > high_score:
            high_score = score

        # Update the score on the score board.
        pen.clear()
        pen.write(f"Score: {score} \t\t HighScore: {high_score}", font=("Verdana", 15, "normal"), align="center")

        # add a segment
        color_shop = ["#2cb67d", "#2DFE54", "#730039", "#f582ae", "#26F7FD", "#078080", "#FF724C"]
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("circle")
        new_segment.color(random.choice(color_shop))
        new_segment.penup()
        segments.append(new_segment)

    # move the end segment in reverse order
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        if head.direction == "down":
            segments[0].goto(x, y+20)
        if head.direction == "right":
            segments[0].goto(x-20, y)
        if head.direction == "left":
            segments[0].goto(x+20, y)
        if head.direction == "up":
            segments[0].goto(x, y-20)

    # Checks for boundary collition
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        time.sleep(1)
        head.goto(0,0)
        head.direction = "stop"

        # Update score after snake and boundry collision.
        score = 0
        pen.clear()
        pen.write(f"Score: {score} \t\t HighScore: {high_score}", font=("Verdana", 15, "normal"), align="center")

        # hide the segment when snake colide with the boudary
        for segment in segments:
            segment.goto(1000, 1000)
        
        # clear the old segment
        segments = []

    # checks for snake's head to body collision
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(1000, 1000)
            head.direction = "stop"

            # Update score after snake's head and body collision.
            score = 0
            pen.clear()
            pen.write(f"Score: {score} \t\t HighScore: {high_score}", font=("Verdana", 15, "normal"), align="center")
        
            # hide the segments when snake collided with its body or segment
            for segment in segments:
                segment.goto(1000, 1000)
            
            # clear the old segment after collision
            segments = []

    save_current_high_score()
