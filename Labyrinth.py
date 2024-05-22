from gturtle import *
from time import sleep
from sys import exit
from random import randint

CELLSIZE = 40 # Wähle zwischen: 10, 20, 40, 50

# Zeichnet das Grundgitter:
def drawGrid():
    global CELLSIZE
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

#Bei Mausklick eine Zelle schwarz färben.
@onMouseHit
def onClick(x, y):
    # Die Position der Turtle speichern
    turtle_x = getX()
    turtle_y = getY()
    # Zelle schwarz färben
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

def doStep():
    # Einen Schritt nach vorne machen.
    forward(CELLSIZE)
    # Falls die Turtle auf einem schwarzen Feld landet,
    # setzen wir sie wieder zurück und drehen sie dafür.

### MAIN ###

#makeTurtle()
player_sprite_direction = 1
player_sprite = 1
makeTurtle()
hideTurtle()
drawGrid()
# An dieser Stelle könntest du ein Feld als Ziel färben.
# Die Turtle auf ein Anfangsfeld setzen:
setPos(-400 + 5*CELLSIZE // 2 , -300 + 5*CELLSIZE // 2 -1)
penUp()
repeat 1000:
    doStep()
    if getPixelColorStr() == "red" :
        print("Du hast gewonnen!!!")
        exit()
    elif getPixelColorStr() != "white":
        back(CELLSIZE)
        right(90)
        player_sprite_direction += 1
        if player_sprite_direction > 4 :
            player_sprite_direction = 1
    if player_sprite_direction == 1 :
        
        if player_sprite == 1 :
            drawImage("u:/Eigene Dateien/sprite_r_1.png")
            player_sprite = 2
        elif player_sprite == 2: 
            drawImage("u:/Eigene Dateien/sprite_r_2.png")
            player_sprite = 3
        elif player_sprite == 3: 
            drawImage("u:/Eigene Dateien/sprite_r_1.png")
            player_sprite = 4
        elif player_sprite == 4: 
            drawImage("u:/Eigene Dateien/sprite_r_3.png")
            player_sprite = 1
            
    elif player_sprite_direction == 2 :
        
        if player_sprite == 1 :
            drawImage("u:/Eigene Dateien/sprite_d_1.png")
            player_sprite = 2
        elif player_sprite == 2: 
            drawImage("u:/Eigene Dateien/sprite_d_2.png")
            player_sprite = 3
        elif player_sprite == 3: 
            drawImage("u:/Eigene Dateien/sprite_d_1.png")
            player_sprite = 4
        elif player_sprite == 4: 
            drawImage("u:/Eigene Dateien/sprite_d_3.png")
            player_sprite = 1

				if player_sprite_direction == 3 :
        
        if player_sprite == 1 :
            drawImage("u:/Eigene Dateien/sprite_l_1.png")
            player_sprite = 2
        elif player_sprite == 2: 
            drawImage("u:/Eigene Dateien/sprite_l_2.png")
            player_sprite = 3
        elif player_sprite == 3: 
            drawImage("u:/Eigene Dateien/sprite_l_1.png")
            player_sprite = 4
        elif player_sprite == 4: 
            drawImage("u:/Eigene Dateien/sprite_l_3.png")
            player_sprite = 1
            
    elif player_sprite_direction == 4 :
        
        if player_sprite == 1 :
            drawImage("u:/Eigene Dateien/sprite_u_1.png")
            player_sprite = 2
        elif player_sprite == 2: 
            drawImage("u:/Eigene Dateien/sprite_u_2.png")
            player_sprite = 3
        elif player_sprite == 3: 
            drawImage("u:/Eigene Dateien/sprite_u_1.png")
            player_sprite = 4
        elif player_sprite == 4: 
            drawImage("u:/Eigene Dateien/sprite_u_3.png")
            player_sprite = 1
    sleep(0.5)
    drawImage("u:/Eigene Dateien/White.png")
    
    
           