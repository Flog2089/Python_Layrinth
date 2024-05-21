from gturtle import *
class Button(object):
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
        
        self.bind_on_click()
        
        
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
        
    
    def bind_on_click(self):
        # Define the method that will be decorated and bound
        @onMouseHit
        def onClick(x, y):
            if self.posX - self.width / 2 < x < self.posX + self.width / 2 and self.posY > y > self.posY - self.height:
                self.click_action()
            else:
                pass
        
        # Assign the decorated method to an instance variable
        self.onClick = onClick
        
    def click_action(self):
        print("hit")