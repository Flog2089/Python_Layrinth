from gturtle import *
from time import sleep
from sys import exit
from random import randint
from modButtons import Button

PLAYGROUND_HEIGHT = 1000
PLAYGROUND_WIDTH = 1400
CELLSIZE = 40 # Wähle zwischen: 10, 20, 40, 50
game_loop = False
difficulty = 0
makeTurtle("u:/Eigene Dateien/Downloads/Duo.jpg")

setPlaygroundSize(PLAYGROUND_WIDTH,PLAYGROUND_HEIGHT)


class difficultyButton(Button):
    def __init__(self, posX, posY, width, height, color, text, difficulty):
        self.difficulty = difficulty
        super(difficultyButton, self).__init__(posX, posY, width, height, color, text)
        
        
    def click_action(self):
        global difficulty
        global game_loop
        difficulty = self.difficulty
        game_loop = True
        print(self.difficulty)
        
        
# Zeichnet das Grundgitter:
def drawGrid():
    global CELLSIZE
    CELLSIZE = 50 - 5 * difficulty
    hideTurtle()
    pd()
    setPenColor("gray")
    x = -PLAYGROUND_WIDTH / 2
    for i in range(PLAYGROUND_WIDTH // CELLSIZE + 1):
        setPos(x + i * CELLSIZE, -PLAYGROUND_HEIGHT / 2)
        moveTo(x + i * CELLSIZE, +PLAYGROUND_HEIGHT / 2)
    y = -PLAYGROUND_HEIGHT / 2
    for i in range(PLAYGROUND_HEIGHT // CELLSIZE + 1):
        setPos(-PLAYGROUND_WIDTH / 2, y + i * CELLSIZE)
        moveTo(+PLAYGROUND_WIDTH / 2, y + i * CELLSIZE)
        
    setPos(10,10)
    setFillColor("red")
    fill()
    setPos(0, 0)
    showTurtle()

#Bei Mausklick eine Zelle schwarz färben.
@onMouseHit
def onClick(x, y):
    if not game_loop:
        difficultyButton.handle_click(x, y)
    else:
        # Die Position der Turtle speichern
        turtle_x = getX()
        turtle_y = getY()
        if game_loop:
            # Zelle schwarz färben
            hideTurtle()
            setPos(x, y)
            if getPixelColorStr() == "white":
                setFillColor("black")
                fill()
            elif getPixelColorStr() == "black":
                setFillColor("white")
                fill()
            # Die Turtle wieder dahin zurücksetzen,
            # wo sie am Anfang war.
            setPos(turtle_x, turtle_y)
            showTurtle()

def doStep():
    global game_loop
    hideTurtle()
    # Einen Schritt nach vorne machen.
    forward(CELLSIZE)
    # Falls die Turtle auf einem schwarzen Feld landet,
    # setzen wir sie wieder zurück und drehen sie dafür.
    try:
        if getPixelColorStr() == "black":
            back(CELLSIZE)
            right(90)
        elif getPixelColorStr() == "red" :
            print("Du hast gewonnen!!!")
            showTurtle()
            exit()
        showTurtle()
    except:
        print("you failed")
        game_loop = False

def start_screen():
    hideTurtle()

    setPenColor("black")
    penUp()
    setPos(0, 330)
    clean("#777777")
  
    label("Greetings, esteemed player!", adjust = "c")
    back(30)
    label("To ensure a smooth and delightful experience,", adjust = "c")
    back(30)
    label("kindly navigate to Form ICA34b,", adjust = "c")
    back(30)
    label("\"New Player Acceptance and Biscuit Preference Survey.\"", adjust = "c")
    back(30)
    label("Two notarized copies are required.", adjust = "c") 
    back(30)
    label("Upon successful completion,", adjust = "c") 
    back(30)
    label("a designated Game Official will be dispatched", adjust = "c") 
    back(30)
    label("to verify your left-handed dominance (a technical requirement).", adjust = "c") 
    back(30)
    label("We value your patience and enthusiasm!", adjust = "c") 
    back(30)    
    
    setPos(0, -100)   
    setPenColor("dark grey") 
    label("Select difficulty:", adjust = "c")    
    
    easy_button = difficultyButton(-250, -200, 200, 100, "green", "Easy", 1)
    easy_button.make()
    
    medium_button = difficultyButton(0, -200, 200, 100, "yellow", "Medium", 2)
    medium_button.make()
    
    hard_button = difficultyButton(250, -200, 200, 100, "red", "Hard", 3)
    hard_button.make()
    
        

start_screen()
while not game_loop:
    pass

if game_loop:
    clear()
    showTurtle()
    drawGrid()
    # An dieser Stelle könntest du ein Feld als Ziel färben.
    # Die Turtle auf ein Anfangsfeld setzen:
    setPos(-PLAYGROUND_WIDTH / 2 + 5*CELLSIZE // 2, -PLAYGROUND_HEIGHT / 2 + 5*CELLSIZE // 2)
    penUp()
    while game_loop:
        doStep()
        sleep(0.7 - 0.2 * difficulty)     