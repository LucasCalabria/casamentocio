import random
import copy

from Food import Food
from Vehicle import Vehicle
from PriorityQueue import PriorityQueue

# areia = 1
# atoleiro = 5
# agua = 10

d = 60
tileMapBkp = []
state = "menu"
path = []
visited = []
frontier = []
minDistances = {}
printPath = []
drawLoop = 0
start= "77"
goal = "00"

def setup():
    global vehicle
    global food
    global tileMap
    global tileMapBkp
    global rows
    global cols
    global pathPosition
    global start
    global goal
    
    pathPosition = 0
    rows, cols = 10, 15
    
    tileMap = [[random.randint(0, 6) for c in range(cols)] for r in range(rows)]
    tileMap[0][0] = 0
    tileMap[7][7] = 0
        
    tileMapBkp = copy.deepcopy(tileMap)
    
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
    
    size(900, 600)
    velocity_vehicle = PVector(0, 0)
    velocity_food = PVector(0, 0)
    vehicle = Vehicle(450, 450, velocity_vehicle)
    food = Food(30, 30, velocity_food)

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
    global current
    global currentNode
    global currentNodeAux
    global minDistances
    global predecessor
    global queue
    global printPath
    global frontierPQ
    global cost_so_far
    global stack
    
    for r in range(rows):
        for c in range(cols):
            rectMode(CENTER)
            noStroke()
            if (tileMap[r][c] == 0 or tileMap[r][c] == 1):
                fill(190,190,50)

            if tileMap[r][c] == 2 or tileMap[r][c] == 3:
                fill(230, 230, 30)

            if tileMap[r][c] == 4 or tileMap[r][c] == 5:
                fill(255, 255, 0)

            if tileMap[r][c] == 6:
                fill(0,0,0)
                
            rect(c * d + d/2, r * d + d/2, d, d)
            
    for v in visited:
        r = int(v[0])
        c = int(v[1:])
        
        rectMode(CENTER)
        fill(0, 170)
        rect(c * d + d/2, r * d + d/2, d, d)
        
    for f in frontier:
        r = int(f[0])
        c = int(f[1:])
        
        rectMode(CENTER)
        fill(0,255, 0, 100)
        rect(c * d + d/2, r * d + d/2, d, d)
        
    for p in printPath:
        r = int(p[0])
        c = int(p[1:])
        
        rectMode(CENTER)
        fill(255,204, 255)
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

        textSize(16)
        texto = "2 - Busca em profundidade"
        text (texto, 30,100)

        textSize(16)
        texto = "3 - Busca em custo uniforme"
        text (texto, 30,125)

        textSize(16)
        texto = "4 - Busca em gulosa"
        text (texto, 30,150)

        textSize(16)
        texto = "5 - Busca em A*"
        text (texto, 30,175)
        
        f_position = food.getPosition()
        v_position = vehicle.getPosition()
        
        visited = []
        printPath = []
        frontier = []
        frontier.append(start)
        
        if keyPressed:
            if key == '1':
                came_from = dict()
                came_from[start] = None
                state = "bfs"
                
            if key == '2':
                came_from = dict()
                came_from[start] = None
                drawLoop = 0
                state = "dfs"
                        
            if key == '3':
                frontierPQ = PriorityQueue()
                frontierPQ.put(start, 0)
                
                came_from = dict()
                cost_so_far = dict()
                came_from[start] = None                
                cost_so_far[start] = 0
                
                state = 'busca uniforme'
                
            if key == '4':
                frontierPQ = PriorityQueue()
                frontierPQ.put(start, 0)
                
                came_from = dict()
                came_from[start] = None
                
                state = 'busca gulosa'
                
            if key == '5':
                frontierPQ = PriorityQueue()
                frontierPQ.put(start, 0)
                
                came_from = dict()
                cost_so_far = dict()
                came_from[start] = None
                cost_so_far[start] = 0
                
                state = "A*"
                
    if (state == "bfs"):
        if not (frontier == []):
            current = frontier.pop(0)
                
            if current == goal:
                getPath(start, goal, came_from)
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
                fill(0,255, 0, 100)
                rect(c * d + d/2, r * d + d/2, d, d)
    
            for next in vizinho(current):
                if next not in came_from:
                    frontier.append(next)
                    came_from[next] = current
                    
        else:
            gethpath(start, goal, came_from)
            drawLoop = 0
            state = "print path"
            
    if (state == "dfs"):
        if (drawLoop % 1 ==0):
            if not (frontier == []):
                current = frontier.pop()
                    
                if current == goal:
                    getPath(start, goal, came_from)
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
                    fill(0,255, 0, 100)
                    rect(c * d + d/2, r * d + d/2, d, d)
        
                for next in vizinho(current):
                    if next not in came_from:
                        frontier.append(next)
                        came_from[next] = current
                        
            else:
                gethPath(start, goal, came_from)
                drawLoop = 0
                state = "print path"
                
        drawLoop += 1
                
    if (state == "busca uniforme"):
        if(drawLoop % 1 == 0):
            if not frontierPQ.empty():
                current = frontierPQ.get()
                
                visited.append(current)
                #frontier.remove(current)
                
                r = int(current[0])
                c = int(current[1:])
                
                rectMode(CENTER)
                fill(255,0,0)
                rect(c * d + d/2, r * d + d/2, d, d)
    
                if current == goal:
                    drawLoop = 0
                    state = "print path"
                    getPath(start, goal, came_from)
                    
                for next in vizinho(current):
                    #frontier.append(next)
    
                    new_cost = cost_so_far[current] + peso(next)
                    if next not in cost_so_far or new_cost < cost_so_far[next]:
                        cost_so_far[next] = new_cost
                        priority = new_cost
                        frontierPQ.put(next, priority)
                        came_from[next] = current
                        
            else:
                getPath(start, goal, came_from)
                drawLoop = 0
                state = "print path"
        drawLoop += 1
    
    if (state == 'busca gulosa'):
        if not frontierPQ.empty():
            current = str(frontierPQ.get())
            visited.append(current)
            
            r = int(current[0])
            c = int(current[1:])
                
            rectMode(CENTER)
            fill(255,0,0)
            rect(c * d + d/2, r * d + d/2, d, d)
            
            if current == goal:
                drawLoop = 0
                getPath(start, goal, came_from)
                state = "print path"
                
            for next in vizinho(current):
                if next not in came_from:
                    priority = heuristic(goal, next)
                    frontierPQ.put(next, priority)
                    came_from[next] = current
        else:
            drawLoop = 0
            getPath(start, goal, came_from)
            state = "print path"
            
    if (state == "A*"):
        if not frontierPQ.empty():
            current = frontierPQ.get()
            
            visited.append(current)
            
            r = int(current[0])
            c = int(current[1:])
                
            rectMode(CENTER)
            fill(255,0,0)
            rect(c * d + d/2, r * d + d/2, d, d)
            
            if current == goal:
                drawLoop = 0
                getPath(start, goal, came_from)
                state = "print path"
                
            for next in vizinho(current):
                new_cost = cost_so_far[current] + peso(next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(goal, next)
                    frontierPQ.put(next, priority)
                    came_from[next] = current
            
    if (state == "print path"):
        if(drawLoop % 1 == 0):
            printPath.append(path[drawLoop/10])
                
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
            
            while True:
                y = random.randint(0, rows-1)
                x = random.randint(0, cols-1)
                if tileMap[y][x] != 6: break
                
            start = goal
            goal = str(y) + str(x)
            
            position = PVector(x * d + d/2, y * d + d/2)
            food.collision(position)


    if not state == 'menu':
        food.display()
        vehicle.display()
        
    
def getPath(start, goal, came_from):
    global path
    
    current = goal
    path = []
    
    while current != start: 
        path.append(current)
        current = came_from[current]

    path.append(start) # optional
    path.reverse() # optional
    
    return path

def vizinho(start):
    global tileMapBkp
    paths = []
    r = int(start[0])
    c = int(start[1:])
    
    if tileMapBkp[r][c] != 6:
        if (r > 0 and tileMap[r-1][c] != 6):
            paths.append(str(r-1)+str(c))
                    
        if (r < 9 and tileMap[r+1][c] != 6):
            paths.append(str(r+1)+str(c))
                    
        if (c > 0 and tileMap[r][c-1] != 6):
            paths.append(str(r)+str(c-1))
                    
        if (c < 14 and tileMap[r][c+1] != 6):
            paths.append(str(r)+str(c+1))
            
    return paths

def peso(position):
    global tileMapBkp
    
    r = int(position[0])
    c = int(position[1:])
    
    if (tileMap[r][c] == 0 or tileMap[r][c] == 1):
        return 1

    if tileMap[r][c] == 2 or tileMap[r][c] == 3:
        return 5

    if tileMap[r][c] == 4 or tileMap[r][c] == 5:
        return 10

    return 1000

def heuristic(a, b):
   # Manhattan distance on a square grid
   ay = int(a[0])
   ax = int(a[1:])
   
   by = int(b[0])
   bx = int(b[1:])
   
   return abs(ax - bx) + abs(ay - by)
