from gturtle import *
#erstellen von Ursprungs - Class von allen Buttons (alle zukünftigen Buttons werden (teilweise über mehrere Ecken) manche dieser properties, Funktionen, etc. vererben) 
#bei weiteren fragen:
# - https://www.w3schools.com/python/python_classes.asp
# - https://www.w3schools.com/python/python_inheritance.asp
# - https://stackoverflow.com/questions/38963018/typeerror-super-takes-at-least-1-argument-0-given-error-is-specific-to-any
class Button(object):
    #die buttons class bekommt eine Liste (Buttons) zugewiesen, in der in Zukunft alle Buttons gespeichert werden
    buttons = []
    #die init Funktion wird bei der Initialisierung von jedem Objekt der class aufgerufen und in ihr werden alle properties dem Objekt zugeordnet
    def __init__(self, posX, posY, width, height, color, text, radius):
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.text = text
        self.color = makeColor(color)
        self.is_working = True
        self.radius = radius
        
        hideTurtle()
        setPenWidth(3)
        setPenColor(self.color)
        setFillColor(self.color)
        #das Objekt fügt sich selber der Liste an Buttons an
        self.buttons.append(self)
        #führt die eigene Funktion aus (s.u.), um sich selbst zu erstellen
        self.rounded_make()
        
    #veraltete Funktion zum erstellen der selbst, wird nicht verwendet, also auch nicht kommentiert
    def make(self):
        setFontSize(24)
        heading(0)
        pd()
        setPos(self.posX, self.posY)
        moveTo(self.posX - self.width / 2, self.posY)
        lt(90)
        fd(self.height)
        lt(90)
        fd(self.width)
        lt(90)
        fd(self.height)
        lt(90)
        fd(self.width / 2)
        rt(90)
        pu()
        bk(self.height / 2)
        fill()
        
        label(self.text, adjust = "c")
        
    #diese Funktion wir verwendet, um die Buttons zu erstellen (mit abgerundeten ecken)
    def rounded_make(self):
        setFontSize(24)
        heading(-90)
        pd()
        setPos(self.posX, self.posY)
        #zentrieren des Buttons auf der X, aber nicht auf der y achse
        fd(self.width / 2 - self.radius)
        #erzeugt Rundungen bei den Ecken des buttons, während dieser gezeichnet wird (Berechnungen & modifizierter Code von chatGPT)
        for _ in range(23):
            fd((self.radius * 3.14159 / 180) * 3.91)
            rt(-3.91)
        fd(self.height - self.radius * 2)
        for _ in range(23):
            fd((self.radius * 3.14159 / 180) * 3.91)
            rt(-3.91)
        fd(self.width- self.radius * 2)
        for _ in range(23):
            fd((self.radius * 3.14159 / 180) * 3.91)
            rt(-3.91)
        fd(self.height- self.radius * 2)
        for _ in range(23):
            fd((self.radius * 3.14159 / 180) * 3.91)
            rt(-3.91)
        #bewegt turtle in die Mitte des Buttons, füllt diesen mit der füllfarbe und macht mit Label den dazugehörigen Text in die Mitte 
        fd(self.width / 2 - self.radius)
        rt(90)
        pu()
        bk(self.height / 2)
        fill()
        setPenColor("black")
        label(self.text, adjust = "c")
        
    #funktion um den button unbrauchbar zu machen
    def destroy(self):
        self.is_working = False
        
    #funktion um den button wieder brauchbar zu machen
    def undestroy(self):
        self.is_working = False

    #classmethod (eine Funktion, welche nicht mit einzelnen Objekten der Klasse, sondern mit der Klasse selbst assoziiert ist), welche durch die klasseneigene Liste durchgeht, und bei jedem Button in der liste checkt, ob dieser angeklickt wurde, wenn ja wird die click Action dieses Buttons ausgeführt (classmethod konzept von chatgpt)
    @classmethod
    def handle_click(cls, x, y):
        for button in cls.buttons:
            if button.posX - button.width / 2 < x < button.posX + button.width / 2 and button.posY > y > button.posY - button.height:
                if button.is_working:
                    button.click_action()
    
    #default click Action zum debuggen (wird später überschrieben)
    def click_action(self):
        print("hit")
        
        
# lokaler onmousehit dekorator, im finalen projekt glaub ich irrelevant, nur debugging
@onMouseHit
def onClick(x, y):
    Button.handle_click(x, y)

#programm wird nur ausgeführt, wenn das programm direkt ausgeführt wird (sonst wird es ausgeführt, wenn es importiert wird)
if __name__ == "__main__":
    makeTurtle()
    a = Button(0, 0, 200, 100, "green", "hello", 25)