from gturtle import *
class Button(object):
    buttons = []
    def __init__(self, posX, posY, width, height, color, text):
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.text = text
        self.color = makeColor(color)
        
        hideTurtle()
        setPenWidth(3)
        setPenColor("black")
        setFillColor(self.color)
        
        self.buttons.append(self)
        
        
    def make(self):
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
        
    
    @classmethod
    def handle_click(cls, x, y):
        for button in cls.buttons:
            if button.posX - button.width / 2 < x < button.posX + button.width / 2 and button.posY > y > button.posY - button.height:
                button.click_action()
        
    def click_action(self):
        print("hit")
        
        
# Bind the click handler to mouse events
@onMouseHit
def onClick(x, y):
    Button.handle_click(x, y)