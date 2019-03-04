class Enemy:
    
    def __init__(self, speed,color,size,position,direction):
        self.x = position[0]
        self.y = position[1]
        self.color = color
        self.speed = speed
        self.size = size
        self.direction = direction # This is a two tuple ex. (-1,0) would be "left" (0,1) would be "up"

    def move(self):
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

        