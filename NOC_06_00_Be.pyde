# The Nature of Code
# Daniel Shiffman
# http://natureofcode.com
#
# Modified by Filipe Calegario

# Draws a "vehicle" on the screen

import random
import copy

from Food import Food
from Graph import Graph
from Vehicle import Vehicle

tileMapBkp = []
state = "menu"
path = []
visited = []

def setup():
    global vehicle
    global food
    global tileMap
    global tileMapBkp
    global rows
    global cols
    global graph
    global tipoBusca
    global pathPosition
    global start
    global goal
    
    pathPosition = 0
    printPath = True
    
    rows, cols = 10, 15
    tileMap = [[random.randint(0, 6) for c in range(cols)] for r in range(rows)]
    tileMap[0][0] = 0
    tileMap[7][7] = 0
    
    tileMapBkp = copy.deepcopy(tileMap)
    
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
    global path
    global start
    global goal
    global tileMapBkp
    global tileMap
    global state
    global frontier
    global came_from
    global drawLoop
    global visited
    
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
                fill(0,128,0)
            
            if tileMap[r][c] == 7:
                fill(245, 30, 231, 250)
                
            rect(c * d + d/2, r * d + d/2, d, d)
            
    for v in visited:
        r = int(v[0])
        c = int(v[1:])
        
        rectMode(CENTER)
        fill(0, 170)
        rect(c * d + d/2, r * d + d/2, d, d)
        
    
    if (state == "menu"):
        background(0)
        textSize(32)
        fill(255)
        
        texto = "Escolha um modelo de busca:"
        text (texto, 30,50)
        
        textSize(16)
        texto = "1 - Busca em largura"
        text (texto, 30,75)
        
        texto = "2 - Busca em profundidade"
        text (texto, 30,100)
        
        if keyPressed:
            if key == '1':
                frontier = []
                visited = []
                frontier.append(start)
                came_from = dict()
                came_from[start] = None
                state = "bfs"
                
            if key == '2':
                caminhoTemp = []
                visited = []
                state = "dfs"
                        
        f_position = food.getPosition()
        v_position = vehicle.getPosition()
        
        goal = str(int((f_position.y-30)/60)) + str(int((f_position.x-30)/60))
        
    if (state == "bfs"):
        if not (frontier == []):
            current = frontier.pop()
            
            if current == goal:
                bfs(start, goal, came_from)
                drawLoop = 0
                state = "print path"
                
            r = int(current[0])
            c = int(current[1:])
            
            visited.append(current)
                
            rectMode(CENTER)
            fill(255,0,0)
            rect(c * d + d/2, r * d + d/2, d, d)
            
            for x in frontier:
                r = int(x[0])
                c = int(x[1:])
                
                rectMode(CENTER)
                fill(255,0, 0, 100)
                rect(c * d + d/2, r * d + d/2, d, d)

            for next in graph.edges(current):
                if next not in came_from:
                    frontier.append(next)
                    came_from[next] = current
                    
        else:
            bfs(start, goal, came_from)
            drawLoop = 0
            state = "print path"
    
    if (state == "print path"):
        if(drawLoop % 10 == 0):
            i = path[drawLoop/10]
            r = int(i[0])
            c = int(i[1:])
            
            tileMap[r][c] = 7
            if (drawLoop/10 == (len(path)-1)):
                state = "get food"
                
        drawLoop += 1
            
    if (state == "get food" and pathPosition < len(path)):
        i = path[pathPosition]
        r = int(i[0])
        c = int(i[1:])
        
        position = PVector(c * d + d/2, r * d + d/2)
        vehicle.arrive(position)
        vehicle.update()
        
        
        if (vehicle.getPosition().dist(position) <= 5):
            pathPosition +=1
    
        if (food.getPosition().dist(vehicle.getPosition()) <= 7):
            state = "menu"
            drawLoop = 0
            pathPosition = 0
            start = goal
            tileMap = copy.deepcopy(tileMapBkp)
            #velocity_vehicle = PVector(0, 0)
            
            while True:
                y = random.randint(0, rows-1)
                x = random.randint(0, cols-1)
                if tileMap[y][x] != 6: break
                
            position = PVector(x * d + d/2, y * d + d/2)
            food.collision(position)


    if not state == 'menu':
        food.display()
        vehicle.display()
    
def bfs(start, goal, came_from):
    global path
    
    current = goal
    path = []
    
    while current != start: 
        path.append(current)
        current = came_from[current]

    path.append(start) # optional
    path.reverse() # optional
    
    return path

def dfs(start, goal, path, visited):
    path.append(start)
    visited.append(start)
    if start == goal:    #caso estejamos no lugar final, é retornado o vetor de caminho
        return path
    for next in graph.edges(start):
        if next not in visited:
            result = dfs(next, goal, path, visited)
            if result is not None:
                return result
    path.pop()
    return None
