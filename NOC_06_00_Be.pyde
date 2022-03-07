# The Nature of Code
# Daniel Shiffman
# http://natureofcode.com
#
# Modified by Filipe Calegario

# Draws a "vehicle" on the screen

import random
import time
import threading

from Food import Food
from Graph import Graph
from Vehicle import Vehicle

def setup():
    global vehicle
    global food
    global tileMap
    global rows
    global cols
    global graph
    global tipoBusca
    global printPath
    global drawLoop
    global pathPosition
    global start
    global goal
    
    drawLoop = 0
    pathPosition = 0
    printPath = True
    
    rows, cols = 10, 15
    tileMap = [[random.randint(0, 6) for c in range(cols)] for r in range(rows)]
    tileMap[0][0] = 0
    tileMap[7][7] = 0
    
    g = {}
    for r in range(rows):
        for c in range(cols):
            if tileMap[r][c] != 6:
                paths = []
                
                if (r > 0 and tileMap[r-1][c] != 6):
                    paths.append(str(r-1)+str(c))
                    
                if (r < 9 and tileMap[r+1][c] != 6):
                    paths.append(str(r+1)+str(c))
                    
                if (c > 0 and tileMap[r][c-1] != 6):
                    paths.append(str(r)+str(c-1))
                    
                if (c < 14 and tileMap[r][c+1] != 6):
                    paths.append(str(r)+str(c+1))
                
                g[str(r)+str(c)] = {i for i in paths}
                    
    graph = Graph(g)
    
    '''while True:
        if keyPressed:
            if key == '1':
                tipobusca = 1
                break'''
    
    size(900, 600)
    velocity_vehicle = PVector(0, 0)
    velocity_food = PVector(0, 0)
    vehicle = Vehicle(450, 450, velocity_vehicle)
    food = Food(30, 30, velocity_food)
    
    start= "77"
    goal = "00"

def draw():
    global d
    global printPath
    global pathPosition
    global drawLoop
    global path
    global start
    global goal
    
    d = 60
    for r in range(rows):
        for c in range(cols):
            rectMode(CENTER)
            noStroke()
            if (tileMap[r][c] == 0 or tileMap[r][c] == 1):
                fill(194, 178, 128)
                
            if tileMap[r][c] == 2 or tileMap[r][c] == 3:
                fill(161, 202, 241)
                
            if tileMap[r][c] == 4 or tileMap[r][c] == 5:
                fill(121, 68, 59)
                
            if tileMap[r][c] == 6:
                fill(0)
            
            elif tileMap[r][c] == 7:
                fill(245, 30, 231)
                
            rect(c * d + d/2, r * d + d/2, d, d)
    
    food.update()
    vehicle.update()
    
    
    
    if printPath:
        f_position = food.getPosition()
        v_position = vehicle.getPosition()
        
        #start(int((v_position.y-30)/60)) + str(int((v_position.x-30)/60))
        goal = str(int((f_position.y-30)/60)) + str(int((f_position.x-30)/60))
    
        path = bfs(start, goal)
    
    if (drawLoop % 10 == 0 and printPath):
        i = path[drawLoop/10]
        r = int(i[0])
        c = int(i[1:])
        
        tileMap[r][c] = 7
        if (drawLoop/10 == (len(path)-1)):
            printPath = False
            
    if (pathPosition < len(path) and not printPath):
        i = path[pathPosition]
        r = int(i[0])
        c = int(i[1:])
        
        position = PVector(c * d + d/2, r * d + d/2)
        vehicle.arrive(position)
        
        if (vehicle.getPosition().dist(position) <= 5):
            pathPosition +=1
        
    food.display()
    vehicle.display()
    
    if (food.getPosition().dist(vehicle.getPosition()) <= 7):
        drawLoop = 0
        pathPosition = 0
        printPath = True
        start = goal
        
        while True:
            y = random.randint(0, rows-1)
            x = random.randint(0, cols-1)
            if tileMap[y][x] != 6: break
            
        position = PVector(y * d + d/2, x * d + d/2)
        food.collision(position)
        
    drawLoop += 1
    
def bfs(start, goal):
    frontier = []
    frontier.append(start)
    came_from = dict()
    came_from[start] = None

    while not frontier == []:
        current = frontier.pop()
        for next in graph.edges(current):
            if next not in came_from:
                frontier.append(next)
                came_from[next] = current
                
    current = goal
    path = []
    while current != start: 
        path.append(current)
        current = came_from[current]

    path.append(start) # optional
    path.reverse() # optional
    
    return path
