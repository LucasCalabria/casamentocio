# The Nature of Code
# Daniel Shiffman
# http://natureofcode.com
#
# Modified by Filipe Calegario

# Draws a "vehicle" on the screen

import random

from Vehicle import Vehicle
from Food import Food

def setup():
    global vehicle
    global food
    global tileMap
    global flag
    
    flag = True
    rows, cols = 64, 36
    tileMap = [([0]*cols) for i in range(rows)]
    
    size(640, 360)
    velocity_vehicle = PVector(0, 0)
    velocity_food = PVector(0, 0)
    vehicle = Vehicle(width / 2, height / 2, velocity_vehicle)
    food = Food(width / 5, height / 5, velocity_food)

def draw():
    background(194, 178, 128)
    global flag
    global centerWater_x
    global centerWater_y
    global tilesWaterNum
    
    global centerObst_x
    global centerObst_y
    global tilesObstNum
    
    global centerMud_x
    global centerMud_y
    global tilesMudNum
    
    if(flag):
        flag = False
        tilesWaterNum = random.randint(3, 6)
        centerWater_x = []
        centerWater_y = []
        for i in range(tilesWaterNum):
            centerWater_x.append(random.randint(25, 615))
            centerWater_y.append(random.randint(25, 335))
            
        tilesObstNum = random.randint(3, 6)
        centerObst_x = []
        centerObst_y = []
        for i in range(tilesObstNum):
            centerObst_x.append(random.randint(25, 615))
            centerObst_y.append(random.randint(25, 335))
            
        tilesMudNum = random.randint(3, 6)
        centerMud_x = []
        centerMud_y = []
        for i in range(tilesMudNum):
            centerMud_x.append(random.randint(25, 615))
            centerMud_y.append(random.randint(25, 335))
    
    for i in range(tilesWaterNum):
        rectMode(CENTER)
        fill(161, 202, 241)
        rect(centerWater_x[i], centerWater_y[i], 50, 50)
        
    for i in range(tilesObstNum):
        rectMode(CENTER)
        fill(0)
        rect(centerObst_x[i], centerObst_y[i], 50, 50)
        
    for i in range(tilesMudNum):
        rectMode(CENTER)
        fill(121, 68, 59)
        rect(centerMud_x[i], centerMud_y[i], 50, 50)
    
    position = food.getPosition()
    food.update()
    food.display()
    vehicle.update()
    vehicle.display()
    vehicle.arrive(position)
    if (food.getPosition().dist(vehicle.getPosition()) <= 7):
        food.collision()
    
