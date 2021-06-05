from pynput import keyboard
from ExcelUtils import *

import random
import time

keys = []

snake = [] # List of tuples, snake[0] is the tail
foods = [] # List of tuples, position of food

StartX = 10
StartY = 10

SnakeColor = (0,0,0)
BackgroundColor = (100,100,100)
FoodColor = (100,0,0)

# Sleep this amount of time between each iteration
SleepDuration = 0.5

# Generate a food with this probability
FoodGenProb = 0.10

# Square grid
GridSize = 20

# Square cells
CellSizeX = 2.14 # == 20 pix
CellSizeY = 15.00 # == 20 pix

def InitGrid(worksheet):
    for x in range(GridSize):
        for y in range(GridSize):
            cell = XYToCellCoordinates(x, y)
            SetCellSize(worksheet, cell, CellSizeX, CellSizeY)
            FillPixel(worksheet, cell, BackgroundColor)

def InitSnake(worksheet):
    snake.append((StartX, StartY))
    FillPixel(worksheet, XYToCellCoordinates(snake[0][0], snake[0][1]), SnakeColor)

def on_press(key):
    #if key == keyboard.Key.esc:
        #return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k in ['up', 'down', 'left', 'right', keyboard.Key.esc]:  # keys of interest
        keys.append(k)

# Place a new food at position, unless that position is occupied by other food or snake
def PlaceFood(worksheet, xypos):
    if xypos not in foods and xypos not in snake:
        foods.append(xypos)
        FillPixel(worksheet, XYToCellCoordinates(xypos[0],xypos[1]), FoodColor)

def GetSnakeHead():
    return snake[-1]

# Moves snake, returns false if collision occurred and otherwise returns the tail.
def MoveSnake(worksheet, direction: str):
    (x,y) = GetSnakeHead()

    tail = snake.pop(0)
    FillPixel(worksheet, XYToCellCoordinates(tail[0],tail[1]), BackgroundColor)

    if(direction == 'up'):
        y -= 1
    elif(direction == 'down'):
        y += 1
    elif(direction == 'left'):
        x -= 1
    elif(direction == 'right'):
        x += 1

    # Check that we have not collided with self or wall
    if(x >= 0 and y >= 0 and x < GridSize and y < GridSize and not (x, y) in snake):
        snake.append((x,y))
        FillPixel(worksheet, XYToCellCoordinates(x, y), SnakeColor)
        return tail
    else:
        return False


if __name__ == "__main__":
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # start to listen on a separate thread

    worksheet = GetNewWorkSheet()
    InitGrid(worksheet)

    InitSnake(worksheet)

    currentDirection = None
    stop = False
    foodEaten = 0
    while not stop:
        if len(keys) != 0:
            key = keys.pop()

            if key == keyboard.Key.esc:
                stop = True
                print("Exiting")

            if key == 'up':
                currentDirection = 'up'
            elif key == 'down':
                currentDirection = 'down'
            elif key == 'left':
                currentDirection = 'left'
            elif key == 'right':
                currentDirection = 'right'

        tail = None
        if currentDirection is not None:
            tail = MoveSnake(worksheet, currentDirection)
            if not tail:
                stop = True

        # Have we collided with a food item?
        snakeHead = GetSnakeHead()
        if(snakeHead in foods):
            foods.remove(snakeHead)
            foodEaten = foodEaten + 1
            snake.insert(0, tail)
            FillPixel(worksheet, XYToCellCoordinates(tail[0], tail[1]), SnakeColor)

        if random.random() > FoodGenProb:
            x = random.randrange(0,GridSize)
            y = random.randrange(0,GridSize)
            if(not (x,y) in snake and not (x,y) in foods):
                PlaceFood(worksheet, (x,y))

        sleepTime = 0.5
        if foodEaten > 5:
            sleepTime = 0.2 + 0.3/(1 + foodEaten)
        if foodEaten > 10:
            sleepTime = 1.0 / foodEaten
        time.sleep(sleepTime)
    
        PrintText(worksheet, XYToCellCoordinates(GridSize+1, 3), "Score")
        PrintText(worksheet, XYToCellCoordinates(GridSize+1, 4), foodEaten)

    PrintText(worksheet, XYToCellCoordinates(GridSize+1, int(GridSize/2)), "Game Over!")
    quit()