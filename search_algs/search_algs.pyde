# The Nature of Code
# Daniel Shiffman
# http://natureofcode.com
#
# Modified by Filipe Calegario
# Modified by Douglas Pontes

# Draws a "vehicle" on the screen

from Vehicle import Vehicle
from Food import Food
import heapq


#variaveis para o perlinNoise
inc = 0.5
xoff = 0
yoff = 0

mapa = []

def setup():
    global vehicle
    global food
    global foodCount
    global path
    global stepCount
    global algName
    
    foodCount = 0
    stepCount = 0
    size(640, 360)
    velocity = PVector(0, 0)
    drawGraph()
    vehicle = Vehicle(width/2+10, height/2+10, velocity)
    food = Food(random(0,640),random(0,360),PVector(0,0))
    resetPosition(food)
    resetPosition(vehicle)
    path = bfs(((vehicle.position[0])//20,(vehicle.position[1])//20), ((food.position[0])//20,(food.position[1])//20))
    algName = "BFS"


def draw():
    global path
    global stepCount
    global foodCount
    global algName
    
    #moveAgent(PVector(path[stepCount][0]*20+10,path[stepCount][1]*20+10))
    #vehicle.position = PVector(path[stepCount][0]*20+10,path[stepCount][1]*20+10)
    if (((vehicle.position[0])//20,(vehicle.position[1])//20) == (path[stepCount][0],path[stepCount][1]) and stepCount < len(path)-1):
        stepCount+=1
    if ((vehicle.position[0])//20,(vehicle.position[1])//20) == ((food.position[0])//20,(food.position[1])//20):
        resetPosition(food)
        foodCount+=1
        if foodCount % 12 < 3:
            path = bfs(((vehicle.position[0])//20,(vehicle.position[1])//20), ((food.position[0])//20,(food.position[1])//20))
            algName = "BFS"
        elif foodCount % 12 < 6:
            path = dfs(((vehicle.position[0])//20,(vehicle.position[1])//20), ((food.position[0])//20,(food.position[1])//20))
            algName = "DFS"
        elif foodCount % 12 < 9:
            path = dijkstra(((vehicle.position[0])//20,(vehicle.position[1])//20), ((food.position[0])//20,(food.position[1])//20))
            algName = "Dijkstra"
        elif foodCount % 12 < 12:
            path = aEstrela(((vehicle.position[0])//20,(vehicle.position[1])//20), ((food.position[0])//20,(food.position[1])//20))
            algName = "A*"
        stepCount = 0
    
    drawGraph()
    updateWorld()
    draw_path()
    drawUI()
    
    fill(255)
    textSize(25)
    text(algName, 10, 25)


def drawUI():
    #background(255)
    fill(255)
    textSize(13)
    text(str(foodCount),vehicle.position[0]+15,vehicle.position[1]+15)
    
def updateWorld():
    global path
    global stepCount
    vehicle.arrive(PVector(path[stepCount][0]*20+10,path[stepCount][1]*20+10))
    vehicle.update()
    vehicle.display()
    food.update()
    food.display()

def resetPosition(object):
    global mapa
    
    while True:
        new_position = PVector(random(0,width),random(0,height))
        if mapa[int(new_position.y/20)][int(new_position.x/20)] <= 10:
            object.position = new_position
            break

def makePath(start, current, came_from):
    path = []
    while current != start: 
        path.append(current)
        stroke(0,255,0)
    
        line(current[0]*20+10,current[1]*20+10,came_from[current][0]*20+10,came_from[current][1]*20+10)
        current = came_from[current]
    path.append(start) # optional
    path.reverse() # optional
    return path

def bfs(start, goal):
    count = 0
    frontier = list()
    frontier.append(start)
    came_from = dict()
    came_from[start] = None
    
    while len(frontier) != 0:
        current = frontier.pop(0)
        for next in graph_neighbors(current):
            if next not in came_from:
                frontier.append(next)
                came_from[next] = current
                if current == goal:
                    break
                #stroke(255,0,0)
                #fill(250,0,0)
                #text(str(count),next[0]*20-15, next[1]*20-15, current[0]*20, current[1]*20)
                count+=1
                #line(next[0]*20, next[1]*20, current[0]*20, current[1]*20)
                #delay(50);
    
    return makePath(start, goal, came_from)

def dfs(start, goal):
    stack = []
    stack.append(start)
    parent = {}
    parent[start] = None
    
    while len(stack) != 0:
        current = stack.pop()
        for neighbor in graph_neighbors(current):
            if neighbor not in parent:
                stack.append(neighbor)
                parent[neighbor] = current
                if current == goal:
                    break
                
    return makePath(start, goal, parent)

def dijkstra(start, goal):
    heap = []
    neighbors = []
    came_from = dict()
    cost_so_far = dict()
    
    came_from[start] = None
    cost_so_far[start] = 0
    heapq.heappush(heap, (0, start))
    while len(heap) != 0:
        current = heapq.heappop(heap)[1]
        if current == goal:
            break
        
        for next in graph_neighbors(current):
            new_cost = cost_so_far[current] + mapa[int(current[1])][int(current[0])]
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                cost = new_cost
                heapq.heappush(heap, (cost, next))
                came_from[next] = current
    
    return makePath(start, goal, came_from)

def aEstrela(start, goal):
    global mapa
    
    heap = []
    heapq.heappush(heap, (0, start))
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0
    
    while len(heap) != 0:
        current = heapq.heappop(heap)[1]
    
        if current == goal:
            break
    
        for next in graph_neighbors(current):
            new_cost = cost_so_far[current] + mapa[int(next[1])][int(next[0])]
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                heapq.heappush(heap, (priority, next))
                came_from[next] = current
    
    return makePath(start, goal, came_from)

def heuristic(a, b):
   # Manhattan distance on a square grid
   return sqrt(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2))

def draw_path():
    global path
    stroke(0,255,0)
    for i in range(len(path)-1):
        line(path[i][0]*20+10,path[i][1]*20+10,path[i+1][0]*20+10,path[i+1][1]*20+10)

    
def graph_neighbors(current):
    global mapa
    neighbors = []
    if(current[0] > 0):
        neighbors.append((current[0]-1,current[1]))
    if(current[1] > 0):
        neighbors.append((current[0],current[1]-1))
    if(current[0] < 31):
        neighbors.append((current[0]+1,current[1]))
    if(current[1] < 17):
        neighbors.append((current[0],current[1]+1))
    if(current[0] > 0 and current[1] > 0):
        neighbors.append((current[0]-1,current[1]-1))
    if(current[0] < 31 and current[1] < 17):
        neighbors.append((current[0]+1,current[1]+1))
    if(current[0] > 0 and current[1] < 17):
        neighbors.append((current[0]-1,current[1]+1))
    if(current[0] < 31 and current[1] > 0):
        neighbors.append((current[0]+1,current[1]-1))
    
    removidos =[]
    for n in neighbors:
        #print(type(n))
        #print(type(n[0]))
        #print(mapa)
        if(mapa[int(n[1])][int(n[0])] > 10):
            removidos.append(n)
    for n in removidos:
        neighbors.remove(n)
    return neighbors
    


    
def drawGraph():
    global inc
    global xoff
    global yoff
    global mapa
    yoff = 0
    mapa = []
    #indices
    for j in range(10,height,20):
        xoff = 0
        row = []
        for i in range(10,width,20):
            xoff+=inc
            cost = 0
            x = noise(xoff,yoff)*40
            if x < 10:
                cost = 1
                fill(68,150,90) #custo baixo caminhar na grama
            elif x < 20:
                cost = 5
                fill(150,75,0) #custo medio caminhar na areia
            elif x < 30:
                cost = 10
                fill(18,10,143) #custo elevado caminhar na agua
            else:
                cost = 99999999
                fill(0)
            row.append(cost)
            #print(x)
            #fill(x)
            stroke(0)
            square(i-10, j-10, 20)
            #fill(0,0,255)
            #circle(i, j, 3)
        yoff+=inc
        mapa.append(row)
    
