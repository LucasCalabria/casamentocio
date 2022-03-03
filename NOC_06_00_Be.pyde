# The Nature of Code
# Daniel Shiffman
# http://natureofcode.com
#
# Modified by Filipe Calegario

# Draws a "vehicle" on the screen

import random

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
    
    rows, cols = 10, 15
    tileMap = [[random.randint(0, 6) for c in range(cols)] for r in range(rows)]
    tileMap[0][0] = 0
    tileMap[7][7] = 0
    
    tileMap[7][6] = 6
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
        
    size(900, 600)
    velocity_vehicle = PVector(0, 0)
    velocity_food = PVector(0, 0)
    vehicle = Vehicle(450, 450, velocity_vehicle)
    food = Food(30, 30, velocity_food)
    
    start = '77'
    goal = '00'
    
    print(bfs(start, goal))

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
                
            rect(c * d + d/2, r * d + d/2, d, d)
    
    position = food.getPosition()
    food.update()
    food.display()
    #vehicle.update()
    vehicle.display()
    vehicle.arrive(position)
    if (food.getPosition().dist(vehicle.getPosition()) <= 7):
        while True:
            y = random.randint(0, rows-1)
            x = random.randint(0, cols-1)
            if tileMap[x][y] != 6: break
            
        position = PVector(y * d + d/2, x * d + d/2)
        food.collision(position)
        
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
