from gturtle import *
#erstellen von Ursprungs - Class von allen Buttons (alle zukünftigen Buttons werden (teilweise über mehrere Ecken) manche dieser properties, Funktionen, etc. vererben) 
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
        fd(self.width / 2 - self.radius)
        rt(90)
        pu()
        bk(self.height / 2)
        fill()
        setPenColor("black")
        label(self.text, adjust = "c")
        
    def destroy(self):
        self.is_working = False
        
    def undestroy(self):
        self.is_working = False

    @classmethod
    def handle_click(cls, x, y):
        for button in cls.buttons:
            if button.posX - button.width / 2 < x < button.posX + button.width / 2 and button.posY > y > button.posY - button.height:
                if button.is_working:
                    button.click_action()
        
    def click_action(self):
        print("hit")
        
        
# Bind the click handler to mouse events
@onMouseHit
def onClick(x, y):
    Button.handle_click(x, y)
    
if __name__ == "__main__":
    makeTurtle()
    a = Button(0, 0, 200, 100, "green", "hello", 25)