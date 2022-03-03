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
    
    flag = False
    rows, cols = 64, 36
    tileMap = [([0]*cols) for i in range(rows)]
    
    size(640, 360)
    velocity_vehicle = PVector(0, 0)
    velocity_food = PVector(0, 0)
    vehicle = Vehicle(width / 2, height / 2, velocity_vehicle)
    food = Food(width / 5, height / 5, velocity_food)

    
    

def draw():
    background(194, 178, 128)
    if(!flag):
        flag = True
        tilesNum = random.randint(0, 20)
        for i in range(1):
            center_x = random.randint(10, 630)
            center_y = random.randint(10, 350)
    
    rectMode(CENTER)
    fill(161, 202, 241)
    rect(center_x, center_y, 50, 50)
    
    position = food.getPosition()
    food.update()
    food.display()
    vehicle.update()
    vehicle.display()
    vehicle.arrive(position)
    if (food.getPosition().dist(vehicle.getPosition()) <= 7):
        food.collision()
    
