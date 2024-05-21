from gturtle import *
from time import sleep
from sys import exit
from random import randint
from modButtons import Button

CELLSIZE = 40 # Wähle zwischen: 10, 20, 40, 50
game_loop = False
difficulty = 0
makeTurtle("u:/Eigene Dateien/Downloads/Duo.jpg")

# Zeichnet das Grundgitter:
def drawGrid():
    global CELLSIZE
    hideTurtle()
    setPenColor("gray")
    x = -400
    repeat (800 // CELLSIZE) + 1:
        setPos(x, -300)
        moveTo(x, +300)
        x += CELLSIZE
    y = -300
    repeat (600 // CELLSIZE) + 1:
        setPos(-400, y)
        moveTo(+400, y)
        y += CELLSIZE
    setPos(1,1)
    setFillColor("red")
    fill()
    setPos(0, 0)
    showTurtle()

#Bei Mausklick eine Zelle schwarz färben.
@onMouseHit
def onClick(x, y):
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
    hideTurtle()
    # Einen Schritt nach vorne machen.
    forward(CELLSIZE)
    # Falls die Turtle auf einem schwarzen Feld landet,
    # setzen wir sie wieder zurück und drehen sie dafür.
    if getPixelColorStr() == "black":
        back(CELLSIZE)
        right(90)
    elif getPixelColorStr() == "red" :
        print("Du hast gewonnen!!!")
        showTurtle()
        exit()
    showTurtle()

### MAIN ###
#makeTurtle()

setPlaygroundSize(800, 800)



class difficultyButton(Button):
    def __init__(self, posX, posY, width, height, color, text, difficulty):
        self.difficulty = difficulty
        super(difficultyButton, self).__init__(posX, posY, width, height, color, text)
        
        
    def click_action(self):
        global difficulty
        global game_loop
        difficulty = self.difficulty
        game_loop = True
        

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
    
    
    setPos(-200, -200)   
    setPenColor("green") 
    label("Easy", adjust = "c")
    easy_button = difficultyButton(-200, -200, 200, 100, "green", "Easy", 1)
    easy_button.make()
    
    setPos(0, -200)   
    setPenColor("yellow") 
    label("Medium", adjust = "c")
    
    setPos(200, -200)   
    setPenColor("red") 
    label("Hard", adjust = "c")
    

        
    

start_screen()
while not game_loop:
    pass

while game_loop:
    clear()
    showTurtle()
    drawGrid()
    # An dieser Stelle könntest du ein Feld als Ziel färben.
    # Die Turtle auf ein Anfangsfeld setzen:
    setPos(-400 + 5*CELLSIZE // 2, -300 + 5*CELLSIZE // 2)
    penUp()
    while True:
        doStep()
        sleep(0.5)     