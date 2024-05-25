from gturtle import *
from time import sleep
from sys import exit
from random import randint

CELLSIZE = 40 # Wähle zwischen: 10, 20, 40, 50

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
player_sprite = 1
makeTurtle()
drawGrid()
# An dieser Stelle könntest du ein Feld als Ziel färben.
# Die Turtle auf ein Anfangsfeld setzen:
setPos(-400 + 5*CELLSIZE // 2 , -300 + 5*CELLSIZE // 2 -1)
penUp()
repeat 1000:
    if player_sprite == 1 :
        drawImage("u:/Eigene Dateien/Downloads/Duo.jpg")
        player_sprite = 2
    else: 
        drawImage("u:/Eigene Dateien/LOLOLOL.png")
        player_sprite = 1
    doStep()
    sleep(0.5)
    
    
           