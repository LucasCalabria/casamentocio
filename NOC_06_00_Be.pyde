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
    global rows
    global cols
    
    flag = True
    rows, cols = 15, 10
    tileMap = [[random.randint(0, 6) for c in range(cols)] for r in range(rows+1)]
    tileMap[0][0] = 0
        
    
    size(900, 600)
    velocity_vehicle = PVector(0, 0)
    velocity_food = PVector(0, 0)
    vehicle = Vehicle(300, 300, velocity_vehicle)
    food = Food(30, 30, velocity_food)

def draw():
    d = 60    
    for r in range(rows):
        for c in range(cols):
            rectMode(CENTER)
            if (tileMap[r][c] == 0 or tileMap[r][c] == 1):
                fill(194, 178, 128)
                
            elif tileMap[r][c] == 2 or tileMap[r][c] == 3:
                fill(161, 202, 241)
                
            elif tileMap[r][c] == 4 or tileMap[r][c] == 5:
                fill(121, 68, 59)
                
            elif tileMap[r][c] == 6:
                fill(0)
                
            rect(r * d + d/2, c * d + d/2, d, d)
    
    position = food.getPosition()
    food.update()
    food.display()
    vehicle.update()
    vehicle.display()
    vehicle.arrive(position)
    if (food.getPosition().dist(vehicle.getPosition()) <= 7):
        while True:
            x = random.randint(0, rows-1)
            y = random.randint(0, cols-1)
            if tileMap[x][y] != 6: break
            
        position = PVector(x * d + d/2, y * d + d/2)
        food.collision(position)
