from gturtle import *

makeTurtle()
class Button:
    def __init__(self, posX, posY, width, height, color, text):
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.text = text
        self.color = makeColor(color)
        self.gurke = makeTurtle()
        
        self.gurke.hideTurtle()
        self.gurke.setPenWidth(3)
        self.gurke.setPenColor("black")
        self.gurke.setFillColor(self.color)
        
        self.bind_on_click()
        
        
    def make(self):
        self.gurke.setPos(self.posX, self.posY)
        self.gurke.moveTo(self.posX - self.width / 2, self.posY)
        self.gurke.lt(90)
        self.gurke.fd(self.height)
        self.gurke.lt(90)
        self.gurke.fd(self.width)
        self.gurke.lt(90)
        self.gurke.fd(self.height)
        self.gurke.lt(90)
        self.gurke.fd(self.width / 2)
        self.gurke.rt(90)
        self.gurke.pu()
        self.gurke.bk(self.height / 2)
        self.gurke.fill()
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
        pass
           
