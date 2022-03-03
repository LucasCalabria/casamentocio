# The "Food" class

import random

class Food():

    def __init__(self, x, y, vel):
        self.acceleration = PVector(0, 0)
        self.velocity = vel
        self.position = PVector(x, y)
        self.r = 8
        self.maxspeed = 1.0
        self.maxforce = 0.01
        self.count = 0

    # Method to update location
    def update(self):
        # Update velocity
        self.velocity.add(self.acceleration)
        # Limit speed
        self.velocity.limit(self.maxspeed)
        self.position.add(self.velocity)
        # Reset accelerationelertion to 0 each cycle
        self.acceleration.mult(0)

    def applyForce(self, force):
        # We could add mass here if we want A = F / M
        self.acceleration.add(force)

    def display(self):
        # Draw a triangle rotated in the direction of velocity
        theta = frameCount / 50.0
        fill(218,165,32)
        noStroke()
        strokeWeight(1)
        with pushMatrix():
            translate(self.position.x, self.position.y)
            rotate(theta)
            self.star()
    
    def collision(self):
        self.position = PVector(random.randint(0, 640), random.randint(0, 360))
        self.count += 1
        print("A comida foi coletada. Total: " + str(self.count))
        
    def getPosition(self):
        return self.position
    
    def star(self):
        radius1 = self.r * 1.3
        radius2 = self.r * 0.6
        npoints = 12
        angle = TWO_PI / npoints
        a = 0
        halfAngle = angle/2.0
        x = 0
        y = 0
        beginShape()
        while (a < TWO_PI):
            sx = x + cos(a) * radius2
            sy = y + sin(a) * radius2
            vertex(sx, sy)
            sx = x + cos(a+halfAngle) * radius1
            sy = y + sin(a+halfAngle) * radius1
            vertex(sx, sy)
            a += angle
        endShape(CLOSE)
