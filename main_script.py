#import von wichtigen libraries
from gturtle import *
from time import sleep
from sys import exit
from random import randint
import os

# Print the current working directory
wd = os.getcwd().replace("\\", "/")
print(wd)
print("{}/sprites/Sprite_d_1.png".format(wd))


player_Sprite_direction = 1
player_Sprite = 1
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
    global player_Sprite_direction
    global player_Sprite
    # Einen Schritt nach vorne machen.
    forward(CELLSIZE)
    # Falls die Turtle auf einem schwarzen Feld landet,
    # setzen wir sie wieder zurück und drehen sie dafür.
    print("step")
    if getPixelColorStr() == "red" :
        print("Du hast gewonnen!!!")
        exit()
    elif getPixelColorStr() != "white":
        back(CELLSIZE)
        right(90)
        player_Sprite_direction += 1
        if player_Sprite_direction > 4 :
            player_Sprite_direction = 1
    if player_Sprite_direction == 1 :

        if player_Sprite == 1 :
            drawImage("{}/sprites/Sprite_r_1.png".format(wd))
            player_Sprite = 2
        elif player_Sprite == 2:
            drawImage("{}/sprites/Sprite_r_2.png".format(wd))
            player_Sprite = 3
        elif player_Sprite == 3:
            drawImage("{}/sprites/Sprite_r_1.png".format(wd))
            player_Sprite = 4
        elif player_Sprite == 4:
            drawImage("{}/sprites/Sprite_r_3.png".format(wd))
            player_Sprite = 1

    elif player_Sprite_direction == 2 :

        if player_Sprite == 1 :
            drawImage("{}/sprites/Sprite_d_1.png".format(wd))
            player_Sprite = 2
        elif player_Sprite == 2:
            drawImage("{}/sprites/Sprite_d_2.png".format(wd))
            player_Sprite = 3
        elif player_Sprite == 3:
            drawImage("{}/sprites/Sprite_d_1.png".format(wd))
            player_Sprite = 4
        elif player_Sprite == 4:
            drawImage("{}/sprites/Sprite_d_3.png".format(wd))
            player_Sprite = 1

    elif player_Sprite_direction == 3 :

        if player_Sprite == 1 :
            drawImage("{}/sprites/Sprite_l_1.png".format(wd))
            player_Sprite = 2
        elif player_Sprite == 2:
            drawImage("{}/sprites/Sprite_l_2.png".format(wd))
            player_Sprite = 3
        elif player_Sprite == 3:
            drawImage("{}/sprites/Sprite_l_1.png".format(wd))
            player_Sprite = 4
        elif player_Sprite == 4:
            drawImage("{}/sprites/Sprite_l_3.png".format(wd))
            player_Sprite = 1

    elif player_Sprite_direction == 4 :

        if player_Sprite == 1 :
            drawImage("{}/sprites/Sprite_u_1.png".format(wd))
            player_Sprite = 2
        elif player_Sprite == 2:
            drawImage("{}/sprites/Sprite_u_2.png".format(wd))
            player_Sprite = 3
        elif player_Sprite == 3:
            drawImage("{}/sprites/Sprite_u_1.png".format(wd))
            player_Sprite = 4
        elif player_Sprite == 4:
            drawImage("{}/sprites/Sprite_u_3.png".format(wd))
            player_Sprite = 1
    sleep(0.5)
    drawImage("{}/sprites/white.png".format(wd))

### MAIN ###

#makeTurtle()

makeTurtle()
hideTurtle()
drawGrid()
# An dieser Stelle könntest du ein Feld als Ziel färben.
# Die Turtle auf ein Anfangsfeld setzen:
setPos(-400 + 5*CELLSIZE // 2 , -300 + 5*CELLSIZE // 2 -1)
penUp()
repeat 1000:
    doStep()




from modButtons import Button

#definition von variablen
PLAYGROUND_HEIGHT = 1000
PLAYGROUND_WIDTH = 1000
CELLSIZE = 40
game_loop = False
difficulty = 0
#turtle wird mit dem angegebenen bild erschaffen
makeTurtle("u:/Eigene Dateien/Downloads/Duo.jpg")

#setzt die größe des turtle fensters auf die oben definierten variablen
setPlaygroundSize(PLAYGROUND_WIDTH,PLAYGROUND_HEIGHT)


#class difficultyButton() mit class Button als parent
class difficultyButton(Button):
    #initialisierung eigener variablen und übernahme von funktionen und variablen von parent
    def __init__(self, posX, posY, width, height, color, text, difficulty):
        self.difficulty = difficulty
        super(difficultyButton, self).__init__(posX, posY, width, height, color, text)

    #eigene definition für aktion wenn geclickt wird (startet spiel und setzt difficulty auf self.difficulty)
    def click_action(self):
        global difficulty
        global game_loop
        difficulty = self.difficulty
        game_loop = True
        print(self.difficulty)


# Zeichnet das Grundgitter:
def drawGrid():
    global CELLSIZE
    CELLSIZE = PLAYGROUND_HEIGHT / (15 + 5 * difficulty)
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

def draw_border():
    ht()
    lt(90)
    pu()
    setFillColor("blue")
    setPos(CELLSIZE / 2, CELLSIZE / 2)
    fd(PLAYGROUND_HEIGHT / 2 - 1 * CELLSIZE)
    rt(90)
    fd(PLAYGROUND_WIDTH / 2 - 1 * CELLSIZE)
    for i in range(2):
        rt(90)
        for j in range((15 + 5 * difficulty) -1):
            fd(CELLSIZE)
            fill()
            print(j, getPos())
        rt(90)
        for j in range((15 + 5 * difficulty) -1):
            fd(CELLSIZE)
            fill()
            print(j, getPos())
    st()
#Bei Mausklick eine Zelle schwarz färben / auf dem Startbilschirm click an button weitergeben
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
#    print(-PLAYGROUND_WIDTH / 2 , getX() , PLAYGROUND_WIDTH / 2)
    # Einen Schritt nach vorne machen.
    fd(CELLSIZE)

    # Falls die Turtle auf einem schwarzen Feld landet,
    # setzen wir sie wieder zurück und drehen sie dafür.
    if getPixelColorStr() == "black":
        back(CELLSIZE)
        right(90)
    elif getPixelColorStr() == "blue":
        back(CELLSIZE)
        rt(180)
    elif getPixelColorStr() == "red" :
        print("Du hast gewonnen!!!")
        showTurtle()
        game_loop = False
        exit()
    showTurtle()

#definition startbildschirm
def start_screen():
    hideTurtle()

    #füllt alles mit einem angenehmen 777777 grau aus
    setPenColor("black")
    penUp()
    setPos(0, 330)
    clean("#777777")

    #code für platzhalter text (danke gemini) wegen fehlendem support für \n im befehl label() in mehrere zeilen aufgeteilt :(
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

    #macht drei knöpfe (s.o.)
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
    draw_border()
    # An dieser Stelle könntest du ein Feld als Ziel färben.
    # Die Turtle auf ein Anfangsfeld setzen:
    setPos(-PLAYGROUND_WIDTH / 2 + 5*CELLSIZE // 2, -PLAYGROUND_HEIGHT / 2 + 5*CELLSIZE // 2)
    penUp()
    showTurtle()
    while game_loop:
        doStep()
        sleep(0.7 - 0.2 * difficulty)