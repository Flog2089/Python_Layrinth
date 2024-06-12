#import von wichtigen libraries
from gturtle import *
from time import sleep
from sys import exit
from random import randint
import os
from modButtons import Button


# Print the current working directory
wd = os.getcwd().replace("\\", "/")

trailing_color = "white"
player_Sprite_direction = 1
player_Sprite = 1
save_slot = 1
sleep_multiplier = 1

slot_selected = False
difficulty_selected = False
dir_right = True
block_loc = []

action_cells = []


#definition von variablen
PLAYGROUND_HEIGHT = 1000
PLAYGROUND_WIDTH = 1000
CELLSIZE = 40
game_loop = False
difficulty = 0
#turtle wird mit dem angegebenen bild erschaffen
makeTurtle("u:/Eigene Dateien/Downloads/Duo.jpg")
enemies = []
bgcolor = "#88AABF"

#setzt die größe des turtle fensters auf die oben definierten variablen
setPlaygroundSize(PLAYGROUND_WIDTH,PLAYGROUND_HEIGHT)




class SlotButton(Button):
    slot_buttons = []
    #initialisierung eigener variablen und übernahme von funktionen und variablen von parent
    def __init__(self, posX, posY, width, height, color, text, border, border_color, radius):
        self.border = border
        self.border_color = border_color
        self.toggle = False
        self.slot_buttons.append(self)
        super(SlotButton, self).__init__(posX, posY, width, height, color, text, radius)
        

    @classmethod
    def unclick(cls, var_to_use = None):
        pass

    #eigene definition für aktion wenn geclickt wird (startet spiel und setzt difficulty auf self.difficulty)
    def click_action(self):
        draw_removable_border()
        SlotButton.unclick()

    def draw_removable_border(self):
        setPenColor(self.border_color)
        setPenWidth(self.border)
        setHeading(0)
        setPos(self.posX, self.posY)
        fd(self.border / 2)
        lt(90)
        pd()
        fd(self.width / 2 - self.radius + self.border / 2)
        for _ in range(23):
            fd((self.radius * 3.14159 / 180) * 3.91)
            rt(-3.91)
        fd(self.height - self.radius * 2 + self.border)
        for _ in range(23):
            fd((self.radius * 3.14159 / 180) * 3.91)
            rt(-3.91)
        fd(self.width- self.radius * 2 + self.border)
        for _ in range(23):
            fd((self.radius * 3.14159 / 180) * 3.91)
            rt(-3.91)
        fd(self.height- self.radius * 2 + self.border)
        for _ in range(23):
            fd((self.radius * 3.14159 / 180) * 3.91)
            rt(-3.91)
        fd(self.width / 2 - self.radius + self.border)
        rt(90)
        pu()
        bk(self.height / 2)
        
    
class SaveSlotButton(SlotButton):
    save_slot_buttons = []
    #initialisierung eigener variablen und übernahme von funktionen und variablen von parent
    def __init__(self, posX, posY, width, height, color, text, slot, border, border_color, radius):
        self.slot = slot
        self.save_slot_buttons.append(self)
        self.saved_score = read_score_return(self.slot)
        self.saved_text = "High Score: " + str(self.saved_score)
        super(SaveSlotButton, self).__init__(posX, posY, width, height, color, text, border, border_color, radius)
        self.make_on_top()


    def make_on_top(self):
        bk(self.height / 3.3)
        setFontSize(19)
        label(self.saved_text, adjust = "c")
        

    @classmethod
    def unclick(cls):
        global save_slot
        for b in cls.save_slot_buttons:
            if b.slot != save_slot:
                setPos(b.posX, b.posY)
                fd(b.border * 0.5)
                setFillColor(bgcolor)
                fill()
                bk(b.border * 0.5)
                b.toggle = False

    #eigene definition für aktion wenn geclickt wird (startet spiel und setzt difficulty auf self.difficulty)
    def click_action(self):
        global save_slot
        save_slot = self.slot
        super(SaveSlotButton, self).draw_removable_border()
        SaveSlotButton.unclick()

class ApplySlotButton(Button):
    #initialisierung eigener variablen und übernahme von funktionen und variablen von parent
    def __init__(self, posX, posY, width, height, color, text, radius):
        super(ApplySlotButton, self).__init__(posX, posY, width, height, color, text, radius)


    def click_action(self):
        global slot_selected
        slot_selected = True

#class DifficultyButton() mit class Button als parent
class DifficultyButton(SlotButton):
    difficulty_buttons = []
    #initialisierung eigener variablen und übernahme von funktionen und variablen von parent
    def __init__(self, posX, posY, width, height, color, text, inner_difficulty, border, border_color, radius):
        self.difficulty = inner_difficulty
        self.difficulty_buttons.append(self)
        super(DifficultyButton, self).__init__(posX, posY, width, height, color, text, border, border_color, radius)
        

    @classmethod
    def unclick(cls):
        global difficulty
        for b in cls.difficulty_buttons:
            if b.difficulty != difficulty:
                setPos(b.posX, b.posY)
                fd(b.border * 0.5)
                setFillColor(bgcolor)
                fill()
                bk(b.border * 0.5)
                b.toggle = False

    #eigene definition für aktion wenn geclickt wird (startet spiel und setzt difficulty auf self.difficulty)
    def click_action(self):
        global difficulty
        difficulty = self.difficulty
        super(DifficultyButton, self).draw_removable_border()
        DifficultyButton.unclick()

class ApplyDifficultyButton(Button):
    #initialisierung eigener variablen und übernahme von funktionen und variablen von parent
    def __init__(self, posX, posY, width, height, color, text, radius):
        super(ApplyDifficultyButton, self).__init__(posX, posY, width, height, color, text, radius)


    def click_action(self):
        global difficulty_selected
        difficulty_selected = True

class BackButton(Button):
    #initialisierung eigener variablen und übernahme von funktionen und variablen von parent
    def __init__(self, posX, posY, width, height, color, text, radius, var):
        self.var = var
        super(BackButton, self).__init__(posX, posY, width, height, color, text, radius)


    def click_action(self):
        global difficulty_selected
        global slot_selected
        global game_running
        if self.var == "difficulty_screen":
            slot_selected = False

        elif self.var == "slot_screen":
            game_running = False
            
class PlayButton(Button):
    #initialisierung eigener variablen und übernahme von funktionen und variablen von parent
    def __init__(self, posX, posY, width, height, color, text, radius):
        super(PlayButton, self).__init__(posX, posY, width, height, color, text, radius)
        self.make_arrow()


    def click_action(self):
        global game_running
        game_running = True
        print("game")
    
    def make_arrow(self):
        
        setPos(self.posX, self.posY - self.height / 2)
        drawImage("{}/sprites/start_arrow.png".format(wd))



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


        setPos(self.pos)
        a = heading()
        setHeading(0)
        setFillColor("white")
        fill()
        drawImage("{}/sprites/{}.png".format(wd, self.sprite))
        if self.pos in action_cells:
            remove_action_cell(self.pos)
        if self.pos in block_loc:
            block_loc.remove(self.pos)
        setHeading(a)
        setPos(turtle_pos)

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
    pos = getPos()
    # Einen Schritt nach vorne machen.
    # Falls die Turtle auf einem schwarzen Feld landet,
    # setzen wir sie wieder zurück und drehen sie dafür.
    if getPixelColorAheadStr(CELLSIZE) == "black":
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
    
    if pos in action_cells:
        action_cell(pos)


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
    setPenWidth(3)
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

    setPos(0, 0)
    showTurtle()
    
    draw_action_cells()

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
        rt(90)
        for j in range(24):
            fd(CELLSIZE)
            fill()
    
#Bei Mausklick eine Zelle schwarz färben / auf dem Startbilschirm click an button weitergeben
@onMouseHit
def onClick(x, y):
    Button.handle_click(x, y)
    if game_loop:
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
#definition Aktions/Fragezeichenfelder
def action_cell(pos):
    global a
    global sleep_multiplier
    global b
    r = randint(1, 3)
    drawImage("{}/sprites/white.png".format(wd))
    if r == 1 :
        doStep()
    elif r == 2:
        sleep_multiplier = 0.3
        b = a
    elif r == 3:
        setPos((randint(-9, 9))*40, (randint(-9, 9))*40)
    remove_action_cell(pos)
    
        
def remove_action_cell(pos):
    try:
        action_cells.remove(pos)
    except:
        pass
    
#definition plazierung der Aktions/Fragezeichenfelder
def draw_action_cells() :
    h = heading()
    setHeading(0)
    for i in range (3 * difficulty) :
        x = (randint(-9, 9))*40
        y = (randint(-9, 9))*40
        setPos(x, y)
        drawImage("{}/sprites/action_sprite.png".format(wd))
        action_cells.append([x, y])
    setHeading(h)



def start_screen():
    clear(bgcolor)
    setPos(0, 350)
    setPenColor("#000000")
    setFont("papyrus", Font.PLAIN, 45)
    label("Welcome to the turtle layrinth", adjust = "c")
    setFont("sans serif", Font.PLAIN, 24)
    
    start_button = PlayButton(0, 75, 150, 150, "green", " ", 30)


def save_slot_selection():
    clear(bgcolor)
    setPos(0, 400)
    setPenColor("black")
    setFontSize(60)
    label("Select your save slot:", adjust = "c")
    slot1_button = SaveSlotButton(0, 250, 250, 150, "#00AAAA", "Slot 1", 1, 10, "#008A8A", 20)
    slot2_button = SaveSlotButton(0, 50, 250, 150, "#009999", "Slot 2", 2, 10, "#007979", 20)
    slot3_button = SaveSlotButton(0, -150, 250, 150, "#008888", "Slot 3", 3, 10, "#006868", 20)
    apply_button = ApplySlotButton(360, -330, 150, 100, "#BB77BB", "Apply", 30)
    slot_back_button = BackButton(-400, 400, 100, 100, "#CCCCCC", "<--", 10, "slot_screen")

def hidden_text():
    setPenColor("black")
    penUp()
    setPos(0, 330)
    
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

#definition startbildschirm
def difficulty_selection():
    clean(bgcolor)
    hideTurtle()
    home()
    setHeading(0)
    
    
        

    #füllt alles mit einem angenehmen 777777 grau aus
    

    #macht drei knöpfe (s.o.)
    setPos(0, 00)
    setPenColor("black")
    label("Select difficulty:", adjust = "c")

    easy_button = DifficultyButton(-250, -50, 200, 100, "#36802D", "Easy", 1, 10, "#16600D", 20)
    medium_button = DifficultyButton(0, -50, 200, 100, "#FFBF00", "Medium", 2, 10, "orange", 20)
    hard_button = DifficultyButton(250, -50, 200, 100, "#BF0000", "Hard", 3, 10, "dark red", 20)
    apply_button = ApplyDifficultyButton(0, -250, 400, 100, "#BB77BB", "Apply" , 20)
    difficulty_back_button = BackButton(-400, 400, 100, 100, "#CCCCCC", "<--", 10, "difficulty_screen")
    

def read_score(save_slot):
    global hi_score
    f = open("saves/save{}.txt".format(save_slot), "r")
    hi_score = int(f.readline())
    f.close()

def read_score_return(save_slot):
    f = open("saves/save{}.txt".format(save_slot), "r")
    hi_score = int(f.readline())
    f.close()
    return hi_score

def save_score(score, save_slot):
    global hi_score
    f = open("saves/save{}.txt".format(save_slot), "w")
    if score > hi_score:
        f.write(str(score))

    elif score < hi_score:
        f.write(str(hi_score))

    f.close()



def change_color_orientation(color):
    pos = getPos()
    for block in block_loc:
        setPos(block)
        setFillColor(color)
        fill()

        setPos(pos)


# DA CODE STARTS RUNNING HERE
game_running = False

while True:
    sleep(0.1)
    start_screen()
    
    while not game_running:
        pass
    
    while game_running:
        sleep(0.1)
        save_slot_selection()
        
        
        while not slot_selected:
            if not game_running:
                for button in Button.buttons:
                    button.destroy()
                break
                
        while slot_selected:
            for button in Button.buttons:
                button.destroy()
                
            difficulty_selection()
            
            while not difficulty_selected:
                if getKey() == "a":
                    hidden_text()
                if not slot_selected:
                    for button in Button.buttons:
                        button.destroy()
                    break
            
            while difficulty_selected:
                for button in Button.buttons:
                    button.destroy()
                
                
                game_loop = True
                player_Sprite_direction = 1
                a = 1
                read_score(save_slot)
                clear()
                showTurtle()
                drawGrid()
                draw_border()
                # An dieser Stelle könntest du ein Feld als Ziel färben.
                # Die Turtle auf ein Anfangsfeld setzen:
                setPos(-PLAYGROUND_WIDTH / 2 + 5*CELLSIZE // 2, -PLAYGROUND_HEIGHT / 2 + 5*CELLSIZE // 2)
                penUp()
                showTurtle()
                setHeading(90)
                b = 0
                pprob.pos = [80, 80]
                while game_loop:
                
                    a += 1
                    ht()
                
                    if a % 2 == 0:
                        pprob.clear_shadow()
                        pprob.advance()
                    pprob.check_catch()
                    doStep()
                    pprob.check_catch()
                    sleep(0.7 - 0.2 * difficulty * sleep_multiplier)
                    setFillColor("white")
                
                    drawImage("{}/sprites/white.png".format(wd))
                    key = getKey()
                    if key == "a":
                        dir_right = False
                        change_color_orientation("green")
                    elif key == "d":
                        dir_right = True
                        change_color_orientation("black")
                
                
                    
                    if a - 5 == b:
                        sleep_multiplier = 1
                        
                
                difficulty_selected = False
                save_score(a, save_slot)
                read_score(save_slot)
                
                               
        
    
    
    
