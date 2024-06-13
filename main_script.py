from gturtle import *
from time import sleep
from sys import exit
from random import *
import os
from modButtons import Button

#der aktuelle dateipfad für workaround beim sprite-system
wd = os.getcwd().replace("\\", "/")

#definieren von variablen
trailing_color = "white"
player_Sprite_direction = 1
player_Sprite = 1
save_slot = 1
sleep_multiplier = 1
difficulty = 0

game_running = False
slot_selected = False
difficulty_selected = False
credits_selected = False
game_loop = False
again = False
combo_breaker = False

dir_right = True
block_loc = []
action_cells = []
enemies = []
death_blocks = []


#setzt die größe des turtle fensters auf die oben definierten variablen
PLAYGROUND_HEIGHT = 1000
PLAYGROUND_WIDTH = 1000
CELLSIZE = 40
bgcolor = "#88AABF"

#turtle wird mit dem angegebenen bild erschaffen (Bild existiert nicht, code nur wegen nostalgie)
setPlaygroundSize(PLAYGROUND_WIDTH,PLAYGROUND_HEIGHT)
makeTurtle("u:/Eigene Dateien/Downloads/Duo.jpg")




#definieren von class slotbutton, welche von parentclass button vererbt
class SlotButton(Button):
    slot_buttons = []
    #initialisierung eigener variablen
    def __init__(self, posX, posY, width, height, color, text, border, border_color, radius):
        self.border = border
        self.border_color = border_color
        self.toggle = False
        #fügt sich selbst einer liste an slotbuttons zu
        self.slot_buttons.append(self)
        #übernahme von funktionen und variablen von parent
        super(SlotButton, self).__init__(posX, posY, width, height, color, text, radius)
        
    #definieren einer methode verfügbar für die ganze klasse (noch leer da später überschrieben wird
    @classmethod
    def unclick(cls, var_to_use = None):
        pass

    #eigene definition für aktion wenn geclickt wird (zeichnet auswahl-rand und entfernt auswahl-rand bei allen anderen knöpfen (wird überschrieben werden)
    def click_action(self):
        draw_removable_border()
        SlotButton.unclick()

    #zeichnet den abgerundeten, entfernbaren auswahlrand
    def draw_removable_border(self):
        setPenColor(self.border_color)
        setPenWidth(self.border)
        setHeading(0)
        setPos(self.posX, self.posY)
        fd(self.border / 2)
        lt(90)
        pd()
        fd(self.width / 2 - self.radius + self.border / 2)
        #komplexe schleifen für abgerundeten rand (ChatGPT als hilfe für berechnungen)
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
        

#definieren von saveslotbutton, welcher von der parentclass slotbutton (oben) erbt
class SaveSlotButton(SlotButton):
    save_slot_buttons = []
    #initialisierung eigener variablen 
    def __init__(self, posX, posY, width, height, color, text, slot, border, border_color, radius):
        self.slot = slot
        #fügt sich selbst einer liste an slotbuttons zu
        self.save_slot_buttons.append(self)
        #liest den highscore von dem zugehörigen slot aus
        self.saved_score = read_score_return(self.slot)
        #macht einen Text zur ausgabe vom highscore
        self.saved_text = "High Score: " + str(self.saved_score)
        #übernahme von funktionen und variablen von parent
        super(SaveSlotButton, self).__init__(posX, posY, width, height, color, text, border, border_color, radius)
        #führt funktion make on top aus (s.u.)
        self.make_on_top()


    #schreibt den highscore unter den slotnamen
    def make_on_top(self):
        bk(self.height / 3.3)
        setFontSize(19)
        label(self.saved_text, adjust = "c")
        

    #eigene classmethod für saveslotbutton
    @classmethod
    def unclick(cls):
        global save_slot
        #der rand von jedem saveslotbutton in der liste der class, welcher nicht dem gerade ausgewählten slot entspricht, wird entfernt
        for b in cls.save_slot_buttons:
            if b.slot != save_slot:
                setPos(b.posX, b.posY)
                fd(b.border * 0.5)
                setFillColor(bgcolor)
                fill()
                bk(b.border * 0.5)
                b.toggle = False

    #eigene definition für aktion wenn geclickt wird (setzt save_slot auf eigenen slot (self.slot) und zeichnet rand)
    def click_action(self):
        global save_slot
        save_slot = self.slot
        #ruft die randzeichnefunktion vom parent auf
        super(SaveSlotButton, self).draw_removable_border()
        #entfernt die ränder von nicht ausgewählten buttons
        SaveSlotButton.unclick()

#definieren von class zum bestätigen von ausgewähltem slot
class ApplySlotButton(Button):
    #s.o.
    def __init__(self, posX, posY, width, height, color, text, radius):
        super(ApplySlotButton, self).__init__(posX, posY, width, height, color, text, radius)

    #fährt fort zum nächsten menüpunkt
    def click_action(self):
        global slot_selected
        slot_selected = True

#definieren class DifficultyButton() mit class Button als parent
class DifficultyButton(SlotButton):
    difficulty_buttons = []
    #s.o.
    def __init__(self, posX, posY, width, height, color, text, inner_difficulty, border, border_color, radius):
        self.difficulty = inner_difficulty
        self.difficulty_buttons.append(self)
        super(DifficultyButton, self).__init__(posX, posY, width, height, color, text, border, border_color, radius)
        

    #siehe SaveSlotButton
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

    #eigene definition für aktion wenn geclickt wird (setzt difficulty auf self.difficulty, rest siehe slotbutton)
    def click_action(self):
        global difficulty
        difficulty = self.difficulty
        super(DifficultyButton, self).draw_removable_border()
        DifficultyButton.unclick()

#definieren class für den save slot bestätigungs button mit class Button als parent
class ApplyDifficultyButton(Button):
    #s.o.
    def __init__(self, posX, posY, width, height, color, text, radius):
        super(ApplyDifficultyButton, self).__init__(posX, posY, width, height, color, text, radius)

    #weiter zum nächsten menüpunkt
    def click_action(self):
        global difficulty_selected
        difficulty_selected = True

#definieren class für den zurück button auf dem game over screen mit class Button als parent
class BackButton(Button):
    #s.o.
    def __init__(self, posX, posY, width, height, color, text, radius, var):
        self.var = var
        super(BackButton, self).__init__(posX, posY, width, height, color, text, radius)

    #abhängig davon welche variable bei erstellen vom Button angegeben wird, werden versch. variablen auf falsch gesetzt, um menüpunkte hoch zu gehen
    def click_action(self):
        global difficulty_selected
        global slot_selected
        global game_running
        global credits_selected
        if self.var == "difficulty_screen":
            slot_selected = False
        elif self.var == "slot_screen":
            game_running = False
            credits_selected = False
        elif self.var == "credits_screen":
            game_running = False

#definieren class für den Start-Knopf auf dem startbildschirm  mit class Button als parent  
class PlayButton(Button):
    #s.o.
    def __init__(self, posX, posY, width, height, color, text, radius):
        super(PlayButton, self).__init__(posX, posY, width, height, color, text, radius)
        self.make_arrow()

    #fährt fort zum nächsten menüpunkt (startet das spiel (slot auswahl))
    def click_action(self):
        global game_running
        global credits_selected
        credits_selected = True
        game_running = True

    #erstellt grünen Pfeil auf startknopf
    def make_arrow(self):
        setPos(self.posX - 7, self.posY - self.height / 2)
        drawImage("{}/sprites/start_arrow.png".format(wd))

#definieren class für den credits button mit class Button als parent
class CreditsButton(Button):
    #s.o
    def __init__(self, posX, posY, width, height, color, text, radius):
        super(CreditsButton, self).__init__(posX, posY, width, height, color, text, radius)

    #"startet das spiel" (geht auf den credits screen)
    def click_action(self):
        global game_running
        game_running = True

#definieren class für den neustart button mit class Button als parent
class AgainButton(Button):
    #s.o.
    def __init__(self, posX, posY, width, height, color, text, radius):
        super(AgainButton, self).__init__(posX, posY, width, height, color, text, radius)

    #startet spiel neu
    def click_action(self):
        global again
        global difficulty_selected
        global slot_selected
        global credits_selected
        global game_loop
        global game_running
        global combo_breaker
        again = True
        slot_selected = False
        difficulty_selected = False
        credits_selected = False
        game_loop = False
        game_running = False
        combo_breaker = False

#definieren class für den beenden button mit class Button als parent
class QuitButton(Button):
    #s.o.
    def __init__(self, posX, posY, width, height, color, text, radius):
        super(QuitButton, self).__init__(posX, posY, width, height, color, text, radius)

    #beendet spiel endgültig
    def click_action(self):
        global combo_breaker
        combo_breaker = True

#definieren für class vom enemy
class Enemy:
    #initialisierung von eigenen variablen für den gegner
    def __init__(self, sprite, posX, posY):
        self.sprite = sprite
        self.posX = posX
        self.posY = posY
        self.pos = [posX, posY]
        self.diff = [0, 0]
        enemies.append(self)
        self.pos_temp = self.pos

    #definieren was passiert, wenn gegner spieler fängt
    def catch_action(self):
        global game_loop
        game_loop = False

    #überprüft, ob gegner spieler gefangen hat
    def check_catch(self):
        if self.pos == getPos():
            #falls gegner spieler fängt, wird die obige catch action ausgeführt
            self.catch_action()

    #funktion zum bewegen vom Gegner
    def advance(self):
        #ruft turtle position ab, um sie später an gleiche position zurückzusetzen
        turtle_pos = getPos()
        a = heading()
        self.pos_temp = self.pos
        #berechnet differenz zur turtle
        self.diff = [self.pos[0] - turtle_pos[0], self.pos[1] - turtle_pos[1]]

        #berechnet, ob gegner nach oben, unten, links, rechts geht (hab ich geschrieben, ohne chatgpt, verstehe den code jedoch nicht mehr, also bei fragen bitte den code kopieren und chatgpt zum erklären geben)
        if abs(self.diff[1]) <= abs(self.diff[0]) and self.diff != [0, 0]:
            self.pos[0] = self.pos[0] - CELLSIZE if (self.diff[0] >= 0) else self.pos[0] + CELLSIZE
        elif abs(self.diff[1]) > abs(self.diff[0]) and self.diff != [0, 0]:
            self.pos[1] = self.pos[1] - CELLSIZE if (self.diff[1] >= 0) else self.pos[1] + CELLSIZE

        #setzt turtle auf eigene position und zeichnet eigene sprite
        setPos(self.pos)
        setHeading(0)
        setFillColor("white")
        fill()
        drawImage("{}/sprites/{}.png".format(wd, self.sprite))
        
        #wenn enemy über einen von den unten genannten blöcken läuft, wird dieser (nicht visuell) im code aus der liste gelöscht
        if self.pos in action_cells:
            remove_action_cell(self.pos)
        if self.pos in block_loc:
            block_loc.remove(self.pos)
            
        #setzt turtle zurück auf position des spielers
        setHeading(a)
        setPos(turtle_pos)

    #übermalt das im vorigen schritt gezeichnete bild von gegner, um keine gegner spur zu hinterlassen (altes bild befindet sich an position self.pos_temp)
    def clear_shadow(self):
        turtle_pos = getPos()
        setPos(self.pos_temp)
        #wird übermalt
        drawImage("{}/sprites/white.png".format(wd))
        setPos(turtle_pos)

#erstellt gegner objekt mit enemy_sprite als sprite auf postition [80, 80]
pprob = Enemy("enemy_sprite", 80, 80)




def doStep():
    #Variablen werden importiert
    global player_Sprite_direction
    global player_Sprite
    global trailing_color
    global death_blocks
    global game_loop
    pos = getPos()
    # Einen Schritt nach vorne machen.
    # Falls die Turtle auf einem schwarzen Feld landet,
    # setzen wir sie wieder zurück und drehen sie dafür.
    if getPixelColorAheadStr(CELLSIZE) == "black":
        right(90)
    #hier wird die richtung festgelegt in die die Turtle guckt
        player_Sprite_direction += 1
        if player_Sprite_direction > 4 :
            player_Sprite_direction = 1
    # Falls die Turtle auf einem Grünen landet,
    # dreht sie sich nach links.
    elif getPixelColorAheadStr(CELLSIZE) == "green":
        lt(90)
    #hier wird die richtung festgelegt in die die Turtle guckt
        player_Sprite_direction -= 1
        if player_Sprite_direction < 1 :
            player_Sprite_direction = 4
    # Falls die Turtle auf einem Blauen Feld landet,
    # dreht sie sich um.
    elif getPixelColorAheadStr(CELLSIZE) == "blue":
        right(180)
    #hier wird die richtung festgelegt in die die Turtle guckt
        player_Sprite_direction += 2
        if player_Sprite_direction > 4 :
            player_Sprite_direction -= 4
    # Turtle geht die eingestellte cellsize nach vorne
    elif game_loop:
        fd(CELLSIZE)
    # Falls man auf einem death block steht wird game_loop auf False gesetzt
    if pos in death_blocks:
        game_loop = False
    # Falls man auf einem Aktionsblock steht wird action_cell ausgeführt
    if pos in action_cells:
        action_cell(pos)

    if game_loop:

    #Guckt in welche richtung der Spieler schaut
        if player_Sprite_direction == 1 :

            #Entscheidet welches Bild angezeigt werden muss für eine flüssige Animation
            if player_Sprite == 1 :
        #Zeichnet Bild
                drawImage("{}/sprites/Sprite_r_1.png".format(wd))
        #setzt fest welches bild als nächstes dran ist
                player_Sprite = 2
            elif player_Sprite == 2:
        #Zeichnet Bild
                drawImage("{}/sprites/Sprite_r_2.png".format(wd))
        #setzt fest welches bild als nächstes dran ist
                player_Sprite = 3
            elif player_Sprite == 3:
        #Zeichnet Bild
                drawImage("{}/sprites/Sprite_r_1.png".format(wd))
        #setzt fest welches bild als nächstes dran ist
                player_Sprite = 4
            elif player_Sprite == 4:
        #Zeichnet Bild
                drawImage("{}/sprites/Sprite_r_3.png".format(wd))
        #setzt fest welches bild als nächstes dran ist
                player_Sprite = 1

    #Guckt in welche richtung der Spieler schaut
        elif player_Sprite_direction == 2 :
            #Entscheidet welches Bild angezeigt werden muss für eine flüssige Animation
            if player_Sprite == 1 :
                #Zeichnet Bild
                drawImage("{}/sprites/Sprite_d_1.png".format(wd))
                #setzt fest welches bild als nächstes dran ist
                player_Sprite = 2
            elif player_Sprite == 2:
                #Zeichnet Bild
                drawImage("{}/sprites/Sprite_d_2.png".format(wd))
                #setzt fest welches bild als nächstes dran ist
                player_Sprite = 3
            elif player_Sprite == 3:
                #Zeichnet Bild
                drawImage("{}/sprites/Sprite_d_1.png".format(wd))
                #setzt fest welches bild als nächstes dran ist
                player_Sprite = 4
            elif player_Sprite == 4:
                #Zeichnet Bild
                drawImage("{}/sprites/Sprite_d_3.png".format(wd))
                #setzt fest welches bild als nächstes dran ist
                player_Sprite = 1

    #Guckt in welche richtung der Spieler schaut
        elif player_Sprite_direction == 3 :

        #Entscheidet welches Bild angezeigt werden muss für eine flüssige Animation
            if player_Sprite == 1 :
        #Zeichnet Bild
                drawImage("{}/sprites/Sprite_l_1.png".format(wd))
        #setzt fest welches bild als nächstes dran ist
                player_Sprite = 2
            elif player_Sprite == 2:
        #Zeichnet Bild
                drawImage("{}/sprites/Sprite_l_2.png".format(wd))
        #setzt fest welches bild als nächstes dran ist
                player_Sprite = 3
            elif player_Sprite == 3:
        #Zeichnet Bild
                drawImage("{}/sprites/Sprite_l_1.png".format(wd))
        #setzt fest welches bild als nächstes dran ist
                player_Sprite = 4
            elif player_Sprite == 4:
        #Zeichnet Bild
                drawImage("{}/sprites/Sprite_l_3.png".format(wd))
        #setzt fest welches bild als nächstes dran ist
                player_Sprite = 1

    #Guckt in welche richtung der Spieler schaut
        elif player_Sprite_direction == 4 :

        #Entscheidet welches Bild angezeigt werden muss für eine flüssige Animation
            if player_Sprite == 1 :
        #Zeichnet Bild
                drawImage("{}/sprites/Sprite_u_1.png".format(wd))
        #setzt fest welches bild als nächstes dran ist
                player_Sprite = 2
            elif player_Sprite == 2:
        #Zeichnet Bild
                drawImage("{}/sprites/Sprite_u_2.png".format(wd))
        #setzt fest welches bild als nächstes dran ist
                player_Sprite = 3
            elif player_Sprite == 3:
        #Zeichnet Bild
                drawImage("{}/sprites/Sprite_u_1.png".format(wd))
        #setzt fest welches bild als nächstes dran ist
                player_Sprite = 4
            elif player_Sprite == 4:
        #Zeichnet Bild
                drawImage("{}/sprites/Sprite_u_3.png".format(wd))
        #setzt fest welches bild als nächstes dran ist
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
    #berechnet wie viele Geraden man braucht und zeichnet diese auf der x achse
    for i in range(PLAYGROUND_WIDTH // CELLSIZE + 1):
        setPos(x + i * CELLSIZE, -PLAYGROUND_HEIGHT / 2)
        moveTo(x + i * CELLSIZE, +PLAYGROUND_HEIGHT / 2)
    y = -PLAYGROUND_HEIGHT / 2
    #berechnet wie viele Geraden man braucht und zeichnet diese auf der y achse
    for i in range(PLAYGROUND_HEIGHT // CELLSIZE + 1):
        setPos(-PLAYGROUND_WIDTH / 2, y + i * CELLSIZE)
        moveTo(+PLAYGROUND_WIDTH / 2, y + i * CELLSIZE)

    setPos(0, 0)
    #zeichnet spezial-Blöcke auf dem spielfeld
    for i in range (3 * difficulty) :
        draw_action_cell()
        draw_death_block()
    
    showTurtle()
#zeichnet die blaue Grenze des Spielbereichs
def draw_border():
    hideTurtle()
    lt(90)
    pu()
    setFillColor("blue")
    #Turtle wird so gesetzt, dass die felder gut ausgefüllt werden können
    setPos(CELLSIZE / 2, CELLSIZE / 2)
    fd(PLAYGROUND_HEIGHT / 2 - 1**1 * CELLSIZE)
    rt(90)
    fd(PLAYGROUND_WIDTH / 2 - 1 * CELLSIZE)
    #füllt die kästchen aus
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
    global block_loc
    #wenn gecklickt wird, sollen alle buttons den klick handeln
    Button.handle_click(x, y)
    #falls das spiel läuft:
    if game_loop:
        #berechnen von der mitte des angeklickten blocks (xxx, yyy)
        xx = (x - 20) // CELLSIZE
        xxx = xx * CELLSIZE + CELLSIZE
        yy = (y - 20) // CELLSIZE
        yyy = yy * CELLSIZE + CELLSIZE
        # Die Position der Turtle speichern
        turtle_x = getX()
        turtle_y = getY()
        # Zelle schwarz färben falls angeclickte zelle weiß ist
        hideTurtle()
        setPos(x, y)
        if getPixelColorStr() == "white":
            if dir_right:
                setFillColor("black")
            else:
                setFillColor("green")
            fill()

            #die koordinate vom block wird der blöcke liste hinzugefügt
            block_loc.append([xxx, yyy])

        #falls hier bereits ein block ist, wird dieser weiß gefärbt und aus der blöckeliste entfernt
        elif getPixelColorStr() == "black" or getPixelColorStr() == "green":
            setFillColor("white")
            fill()
            block_loc.remove([xxx, yyy])


        #turtle wird zurückgesetzt
        setPos(turtle_x, turtle_y)
#definition Aktions/Fragezeichenfelder
def action_cell(pos):
    global a
    global sleep_multiplier
    global b
    #eine zufallszahl wird gewählt, die bestimmt was passieren soll
    r = randint(1, 3)
    drawImage("{}/sprites/white.png".format(wd))
    #boost: schiesst dich 2 felder nach vorne
    if r == 1 :
        doStep()
    #drawimage damit die sprite gelöscht wird auf dem Spielfeld
        drawImage("{}/sprites/white.png".format(wd))
        doStep()
    #verlangsamt den spieler
    elif r == 2:
        sleep_multiplier = 0.3
        b = a
    #teleportiert dich zufällig
    elif r == 3:
        setPos((randint(-9, 9))*40, (randint(-9, 9))*40)
    remove_action_cell(pos)
    draw_action_cell()
    
        
def remove_action_cell(pos):
    try:
        action_cells.remove(pos)
    except:
        pass
    
#definition plazierung der Aktions/Fragezeichenfelder
def draw_action_cell() :
    pos = getPos()
    h = heading()
    setHeading(0)
    
    x = (randint(-9, 9))*40
    y = (randint(-9, 9))*40
    setPos(x, y)
    drawImage("{}/sprites/action_sprite.png".format(wd))
    action_cells.append([x, y])
    setHeading(h)
    setPos(pos)

#funktion zum zeichnen eines einzelen todeskästchens
def draw_death_block():
    global death_blocks
    global action_cells
    #generieren von zufälliger x und y koodinate im raster
    x = (randint(-9, 9))*40
    y = (randint(-9, 9))*40
    #solange ein kästchen mit diesen koordinaten, oder eine action cell mit diesen koordinaten existiert, wird ein neuer block generiert
    while [x, y] in death_blocks or [x, y] in action_cells:
        x = (randint(-10, 9))*40
        y = (randint(-10, 9))*40
    
    turtlePos = getPos()
    setPos(x, y)
    #zeichnen von dem block
    setFillColor("red")
    fill()
    setPos(turtlePos)
    #hinzufügen von den koordinaten in die death_blocks liste
    death_blocks.append([x, y])

#definieren von dem startbildschirm
def start_screen():
    clear(bgcolor)
    #simple texte
    setPos(0, 350)
    setPenColor("#000000")
    setFont("DiMurphic", Font.PLAIN, 65)
    label("Welcome to the turtle layrinth?", adjust = "c")
    setFont("sans serif", Font.PLAIN, 24)
    #zwei buttons für versch. untermenüs
    start_button = PlayButton(0, 75, 150, 150, "green", " ", 30)
    credits_button = CreditsButton(0, -350, 200, 50, "red", "credits", 10)

#definieren von auswahlbildschirm für den speicherstand
def save_slot_selection():
    #färbt den ganzen bildschirm mit der hintergrundfarbe
    clear(bgcolor)
    #macht ein label mit text
    setPos(0, 400)
    setPenColor("black")
    setFontSize(60)
    label("Select your save slot:", adjust = "c")

    #erstellen von 5 button objekten von oben definierten Button classes mit jeweiligen oben angegebenen properties
    #3 reaktive knöpfe zum auswählen von schwierigkeitsgrad
    slot1_button = SaveSlotButton(0, 250, 250, 150, "#00AAAA", "Slot 1", 1, 10, "#008A8A", 20)
    slot2_button = SaveSlotButton(0, 50, 250, 150, "#009999", "Slot 2", 2, 10, "#007979", 20)
    slot3_button = SaveSlotButton(0, -150, 250, 150, "#008888", "Slot 3", 3, 10, "#006868", 20)
    #1 knopf um schwierigkeitsgrad zu bestätigen und fortzufahren
    apply_button = ApplySlotButton(360, -330, 150, 100, "#BB77BB", "Apply", 30)
    # knopf zum rückkehren ins vorige menü
    slot_back_button = BackButton(-400, 450, 100, 100, "#CCCCCC", "<--", 10, "slot_screen")
    
#definieren von menüseite mit credits
def credits_screen():
    #s.o.
    clean(bgcolor)
    ht()
    #erstellen eines back button objektes um credits zu verlassen
    credits_back_buttons = BackButton(-400, 450, 100, 100, "#CCCCCC", "<--", 10, "credits_screen")
    #erstellen von allen texten auf dem credits screen
    setPos(0, 380)
    setFontSize(60)
    label("Credits:", adjust = "c")
    setFontSize(25)
    setPos(0, 270)
    label("Flog - alle Sprites von Hand erstellt, Spieler Frame für Frame animiert, ", adjust = "c")
    setPos(0, 240)
    label("Action Cells für mehr Dynamik eingebaut.", adjust = "c")
    setPos(0, 190)
    label("Doman - Menüsystem von null auf genestet, sich mit dem blauen Rand abge müht,", adjust = "c")
    setPos(0, 160)
    label("den Gegner (pprob) ins Leben gerufen, Blöcke Farben wechseln lassen", adjust = "c")
    setPos(0, 110)
    label("ChatGPT - genervt, weil es Anweisungen nicht verstanden hat", adjust = "c")

    
#wird nicht erklärt, da easter egg
def hidden_text():
    setPenColor("black")
    penUp()
    setPos(0, 430)
    
    #code für den text (danke gemini) wegen fehlendem support für \n im befehl label() in mehrere zeilen aufgeteilt :(
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
    
    setPos(400, 400)
    #https://www.youtube.com/watch?v=dQw4w9WgXcQ
    drawImage("{}/sprites/smol_rick.png".format(wd))

#definieren von schwierigkeiten-auswahlbildschirm
def difficulty_selection():
    #s.o.
    clean(bgcolor)
    hideTurtle()
    #setzt turtle zurück nach hause und nach oben guckend
    setHeading(0)
    home()

    #erstellen von text auf seite
    setPos(0, 100)
    setPenColor("black")
    label("Select difficulty:", adjust = "c")

    #macht 5 knöpfe (s.o.)
    easy_button = DifficultyButton(-250, 50, 200, 100, "#36802D", "Easy", 1, 10, "#16600D", 20)
    medium_button = DifficultyButton(0, 50, 200, 100, "#FFBF00", "Medium", 2, 10, "orange", 20)
    hard_button = DifficultyButton(250, 50, 200, 100, "#BF0000", "Hard", 3, 10, "dark red", 20)
    apply_button = ApplyDifficultyButton(0, -150, 400, 100, "#BB77BB", "Apply" , 20)
    difficulty_back_button = BackButton(-400, 450, 100, 100, "#CCCCCC", "<--", 10, "difficulty_screen")

#definieren von game over bilschirm
def game_over_screen():
    #s.o.
    clean(bgcolor)
    #schreiben von text auf seite
    setPenColor("red")
    setPos(0, 200)
    setFontSize(80)
    label("DU BIST GESTORBEN?", adjust = "c")
    setPos(0, -100)
    setFontSize(50)
    setPenColor("black")
    #schreibt den vorig erreichten score auf dies seite (score wird in "a" gemessen)
    label("Your score: {}".format(a), adjust = "c")
    #erstellen von nochmal und beenden knopf objekten
    again_button = AgainButton(0, -150, 150, 100, "gray", "Again", 20)
    quit_button = QuitButton(0, -300, 150, 100, "red", "Quit", 20)
    

#definieren von funktion zum auslesen von highscore
def read_score(save_slot):
    global hi_score
    #öffnen (im lesemodus) und auslesen von score aus datei mit namen vom aktuell ausgewählten slot
    f = open("saves/save{}.txt".format(save_slot), "r")
    #setzen von hi_score auf die erste zeile in der datei (der high score)
    hi_score = int(f.readline())
    #schließen von datei
    f.close()

#gleich, wie oben, jedoch returnt funktion den gespeicherten wert
def read_score_return(save_slot):
    f = open("saves/save{}.txt".format(save_slot), "r")
    hi_score = int(f.readline())
    f.close()
    return hi_score

#definieren von funktion zum speichern von highscores
def save_score(score, save_slot):
    global hi_score
    #öffnen (im schreibmodus) und schreiben von score in die datei mit namen vom aktuell ausgewählten slot, falls der aktuelle score höher ist als high score
    f = open("saves/save{}.txt".format(save_slot), "w")
    if score > hi_score:
        f.write(str(score))
    elif score < hi_score:
        f.write(str(hi_score))
    #schließen der datei
    f.close()


#definieren von funktion zum ändern der farben der blöcke
def change_color_orientation(color):
    pos = getPos()
    #macht dies bei jedem block in der blöckeliste
    for block in block_loc:
        setPos(block)
        setFillColor(color)
        fill()

    setPos(pos)


# DA CODE STARTS RUNNING HERE

#das menü
#läuft in dauerschleife
while True:
    #wenn combo_breaker true ist wird die dauerschleife verlassen
    if combo_breaker:
        break
    #zeichnet startbildschirm
    start_screen()
    #solange das spiel nicht anfängt zu laufen wird dauerhaft folgendes ausgeführt (turtles laufen über bildschirm)(sodass start_screen nicht die ganze zeit ausgeführt wird
    while not game_running:
        #zufallszahl zwischen 0 und 3
        arand = randint(0, 3)
        #zufallsfarbe aus der liste
        setColor(choice(["red", "blue", "yellow", "green"]))
        #abhängig davon was arand ist, kommt turtle aus versch richtungen & positionen
        if arand == 0:
            #feste x postion außerhalb des bildschirms, jedoch zufällige y koordinate
            setPos(600, randint(-300, 300))
        elif arand == 1:
            setPos(-600, randint(-300, 300))
        elif arand == 2:
            setPos(randint(-300, 300), 600)
        elif arand == 3:
            setPos(randint(-300, 300), -600)
        #und schaut auf einen random punkt auf dem spielfeld
        setHeading(towards(0 + randint(-400, 400), 0 - randint(-400, 400)))
        #wird sichtbar
        st()
        #fragwürdige entwicklungsentscheidungen
        #lässt turtle in mittlerem tempo über spielfeld laufen solange das spiel nicht läuft (also bevor der button angeclickt wird)
        counter = 0
        while not game_running:
            counter += 1
            fd(8)
            if counter == 200:
                break
        #alternative, wobei button click nur registriert wird, nachdem die turtle angekommen ist:
#        for i in range(200):
#            fd(8)
#            if i == 200:
#                break
#
    #sobald das spiel anfängt zu laufen (game_running = true)
    while game_running:
        #s.o.
        if combo_breaker:
            break
        #alle bisherigen buttons in der button.buttons liste werden zerstört (siehe andere datei)
        for button in Button.buttons:
            button.destroy()

        #credits screen wird geladen
        credits_screen()

        #solange die credits noch nicht selected sind läuft folgendes ab
        while not credits_selected:
            #wenn das spiel nicht läuft werden alle buttons zerstört, und die schleife wird verlassen (damit credits_screen() nicht dauerhaft ausgeführt wird)
            if not game_running:
                for button in Button.buttons:
                    button.destroy()
                break

        #fährt fort sobald credits_selected = true
        while credits_selected:
            #s.o.
            if combo_breaker:
                break
            #zeichnet die save slot selection
            save_slot_selection()
            
            #solange slots nicht selected sind wird folgendes ausgeführt:
            while not slot_selected:
                #wenn credits nicht selected sind, werden alle buttons gelöscht und die schleife wird verlassen
                if not credits_selected:
                    for button in Button.buttons:
                        button.destroy()
                    break

            #fährt fort sobald slot_selected = true
            while slot_selected:
                #s.o.
                for button in Button.buttons:
                    button.destroy()
                if combo_breaker:
                    break

                #zeichnet die difficulty selection
                difficulty_selection()
                
                #wird nicht erklärt
                while not difficulty_selected:
                    if getKey() == "p":
                        if getKeyWait() == "a":
                            if getKeyWait() == "i":
                                if getKeyWait() == "n":
                                    hidden_text()
                                    
                    if getKey() == "u":
                        difficulty_selection()

                    #wenn slots nicht selected sind, werden alle buttons gelöscht und die schleife wird verlassen
                    if not slot_selected:
                        for button in Button.buttons:
                            button.destroy()
                        break
                
                #fährt fort sobald difficulty_selected = true
                while difficulty_selected:
                    #s.o.
                    if combo_breaker:
                        break
                    for button in Button.buttons:
                        button.destroy()
                    
                    #setzt die game loop auf true
                    game_loop = True
                    #resettet die player sprite direction
                    player_Sprite_direction = 1
                    #resetet (score) counter
                    a = 1
                    #liest den score aus datei
                    read_score(save_slot)

                    clear()
                    showTurtle()
                    #zeichnet das spielfeld
                    drawGrid()
                    draw_border()
                    # Die Turtle auf ein Anfangsfeld setzen:
                    setPos(-PLAYGROUND_WIDTH / 2 + 5*CELLSIZE // 2, -PLAYGROUND_HEIGHT / 2 + 5*CELLSIZE // 2)
                    penUp()
                    showTurtle()
                    setHeading(90)
                    #setzt referenzwert für das vergehen von zeit auf 0
                    b = 0
                    #gegner pprob wird auf [80, 80] gesetzt
                    pprob.pos = [80, 80]
                    #läuft solange game_loop true ist
                    while game_loop:
                        #variable a wird inkrementiert
                        a += 1
                        #turtle wird zur sicherheit immer wieder versteckt
                        ht()

                        #gegner geht nach vorne, wenn a gerade ist (also bei jedem zweiten spieler-schritt
                        if a % 2 == 0:
                            pprob.clear_shadow()
                            pprob.advance()
                        if a % 10 == 0 :
                            draw_death_block()
                        #gegner überprüft, ob spieler gefangen wurde
                        pprob.check_catch()
                        #wenn game_loop auf falsch gesetzt wird, wird die loop unverzüglich verlassen
                        if not game_loop:
                            break
                        #spieler macht schritt
                        doStep()
                        #gegner überprüft wieder
                        pprob.check_catch()
                        #es wird kurz geschlafen, damit spieler nicht unendlich schnell ist (schlafdauer abhängig von schwierigkeit und effekt-feldern
                        sleep(0.7 - 0.2 * difficulty * sleep_multiplier)
                        #vorherig gemalte spieler-sprite wird übermalt
                        setFillColor("white")
                        drawImage("{}/sprites/white.png".format(wd))
                        #keyboard input für farbwechsel der blöcke
                        key = getKey()
                        #abhängig davon, was der input ist, werden die blöcke entweder grün oder schwarz
                        if key == "a":
                            dir_right = False
                            change_color_orientation("green")
                        elif key == "d":
                            dir_right = True
                            change_color_orientation("black")

                        
                        #falls fünf schritte seit b vergangen sind, wird der sleep_multiplier effekt von den action_cells resettet
                        if a - 5 == b:
                            sleep_multiplier = 1
                            
                    #hier kommt man hin, wenn man stirbt
                    #kurz warten nach tod
                    sleep(1)
                    #speichern und auslesen von score (a)
                    save_score(a, save_slot)
                    read_score(save_slot)
                    #alle variablen zurücksetzten
                    difficulty_selected = False
                    action_cells = []
                    block_loc = []
                    death_blocks = []
                    dir_right = True
                    again = False
                    #game over bildschirm zeichen
                    game_over_screen()
                    #solange warten bis again wahr wird, und wenn auch combo_breaker wahr ist das spiel beenden, falls nicht, zurück zum startbildschirm
                    while not again:
                        if combo_breaker:
                            break
                    
                    
#wird ausgeführt falls spiel beendet wird
#zeichnet den end-screen
clean(bgcolor)
setPos(0, 0)
setFontSize(50)
label("You may now close the turtle window", adjust = "c")


                               
        
    
    

