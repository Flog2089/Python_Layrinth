#import von wichtigen libraries
from gturtle import *
from time import sleep
from sys import exit
from random import randint
import os
from modButtons import Button


# Print the current working directory
wd = os.getcwd().replace("\\", "/")
print("{}/sprites/Sprite_d_1.png".format(wd))

trailing_color = "white"
player_Sprite_direction = 1
player_Sprite = 1
save_slot = 1

dir_right = True
block_loc = []



#definition von variablen
PLAYGROUND_HEIGHT = 1000
PLAYGROUND_WIDTH = 1000
CELLSIZE = 40
game_loop = False
difficulty = 0
#turtle wird mit dem angegebenen bild erschaffen
makeTurtle("u:/Eigene Dateien/Downloads/Duo.jpg")
enemies = []

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
        
        
    
class Enemy:
    def __init__(self, color, difficulty, name, sprite, posX, posY):
        self.color = color
        self.difficutly = difficulty
        self.name = name
        self.sprite = sprite
        self.posX = posX
        self.posY = posY
        self.pos = [posX, posY]
        self.diff = [0, 0]
        enemies.append(self)
        self.pos_temp = self.pos
        
    def catch_action(self):
        global game_loop
        print("caught")
        game_loop = False
        
    def check_catch(self):
        if self.pos == getPos():
            self.catch_action()
    
    def advance(self):
        turtle_pos = getPos()
        self.pos_temp = self.pos
        self.diff = [self.pos[0] - turtle_pos[0], self.pos[1] - turtle_pos[1]]
        
        if abs(self.diff[1]) <= abs(self.diff[0]) and self.diff != [0, 0]:
            self.pos[0] = self.pos[0] - CELLSIZE if (self.diff[0] >= 0) else self.pos[0] + CELLSIZE
        elif abs(self.diff[1]) > abs(self.diff[0]) and self.diff != [0, 0]:
            self.pos[1] = self.pos[1] - CELLSIZE if (self.diff[1] >= 0) else self.pos[1] + CELLSIZE
        
        #print(self.diff)
        
        setPos(self.pos)
        a = heading()
        setHeading(0)
        setFillColor("white")
        fill()
        drawImage("{}/sprites/{}.png".format(wd, self.sprite))
        setHeading(a)
        setPos(turtle_pos)
#        print(self.pos)
#        print(self.pos_temp)

    def clear_shadow(self):
        turtle_pos = getPos()
        setPos(self.pos_temp)
        drawImage("{}/sprites/white.png".format(wd))
        setPos(turtle_pos)
            
pprob = Enemy(1, 1, 1, "enemy_sprite", 80, 80)
            

def doStep():
    global player_Sprite_direction
    global player_Sprite
    global trailing_color
    # Einen Schritt nach vorne machen.
    # Falls die Turtle auf einem schwarzen Feld landet,
    # setzen wir sie wieder zurück und drehen sie dafür.
    if getPixelColorStr() == "red" :
        print("Du hast gewonnen!!!")
        exit()
    elif getPixelColorAheadStr(CELLSIZE) == "black":
        right(90)
        player_Sprite_direction += 1
        if player_Sprite_direction > 4 :
            player_Sprite_direction = 1
    elif getPixelColorAheadStr(CELLSIZE) == "green":
        lt(90)
        player_Sprite_direction -= 1
        if player_Sprite_direction < 1 :
            player_Sprite_direction = 4
        
    elif getPixelColorAheadStr(CELLSIZE) == "blue":
        right(180)
        player_Sprite_direction += 2
        if player_Sprite_direction > 4 :
            player_Sprite_direction -= 4
    else:
        fd(CELLSIZE)
            
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
    

# Zeichnet das Grundgitter:
def drawGrid():
    global CELLSIZE
    CELLSIZE = 40
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
    hideTurtle()
    lt(90)
    pu()
    setFillColor("blue")
    setPos(CELLSIZE / 2, CELLSIZE / 2)
    fd(PLAYGROUND_HEIGHT / 2 - 1 * CELLSIZE)
    rt(90)
    fd(PLAYGROUND_WIDTH / 2 - 1 * CELLSIZE)
    for i in range(2):
        rt(90)
        for j in range(24):
            fd(CELLSIZE)
            fill()
            #print(j, getPos())
        rt(90)
        for j in range(24):
            fd(CELLSIZE)
            fill()
            #print(j, getPos())
    
#Bei Mausklick eine Zelle schwarz färben / auf dem Startbilschirm click an button weitergeben
@onMouseHit
def onClick(x, y):
    if not game_loop:
        difficultyButton.handle_click(x, y)
    else:
        xx = (x - 20) // CELLSIZE
        xxx = xx * CELLSIZE + CELLSIZE
        yy = (y - 20) // CELLSIZE
        yyy = yy * CELLSIZE + CELLSIZE
        # Die Position der Turtle speichern
        turtle_x = getX()
        turtle_y = getY()
        # Zelle schwarz färben
        hideTurtle()
        setPos(x, y)
        if getPixelColorStr() == "white":
            if dir_right:
                setFillColor("black")
            else:
                setFillColor("green")
            fill()
            
            block_loc.append([xxx, yyy])  
            
    
        elif getPixelColorStr() == "black" or getPixelColorStr() == "green":
            setFillColor("white")
            fill()
            block_loc.remove([xxx, yyy]) 
            
            # Die Turtle wieder dahin zurücksetzen,
            # wo sie am Anfang war.
        
        setPos(turtle_x, turtle_y)
        
        
        
    print(block_loc)
          



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


def read_score(save_slot):
    f = open("saves/save{}.txt".format(save_slot), "r")
    hi_score = f .readline()
    f.close()
    return hi_score

def save_score(score, save_slot):
    old_score = int(read_score(save_slot))
    f = open("saves/save{}.txt".format(save_slot), "w")
    if old_score < score:
        f.write(str(score))
        print("yes")
    else:
        f.write(str(old_score))
        print("no")
    f.close()

def change_color_orientation(color):
    pos = getPos()
    for block in block_loc:
        setPos(block)
        setFillColor(color)
        fill()
        
        setPos(pos)


start_screen()
while not game_loop:
    pass

a = 9999999
if game_loop:
    a = 1
    print(read_score(save_slot))
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
        
        a += 1
        ht()
        
        if a % 2 == 0:
            pprob.clear_shadow()
            pprob.advance()
        pprob.check_catch()
        doStep()
        pprob.check_catch()
        sleep(0.7 - 0.2 * difficulty)
        setFillColor("white")
        
        drawImage("{}/sprites/white.png".format(wd))
        
        key = getKey()
        if key == "a":
            dir_right = False
            change_color_orientation("green")
        elif key == "d":
            dir_right = True
            change_color_orientation("black")
                                    
save_score(a, save_slot)
    
    




