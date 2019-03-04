class Player:
    SIZE = 50

    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.color = color

    # Direction is a two tuple
    def move(self,direction):
        self.x += direction[0] * (Player.SIZE/25)
        self.y += direction[1] * (Player.SIZE/25)
