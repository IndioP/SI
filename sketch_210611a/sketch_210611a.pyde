# The Nature of Code
# Daniel Shiffman
# http://natureofcode.com
#
# Modified by Filipe Calegario
# Modified by Douglas Pontes

# Draws a "vehicle" on the screen

from Vehicle import Vehicle
from Food import Food


#variaveis para o perlinNoise
inc = 0.2
xoff = 0
yoff = 0

mapa = []

def setup():
    global vehicle
    global food
    global foodCount
    global path
    global stepCount
    foodCount = 0
    stepCount = 0
    size(640, 360)
    velocity = PVector(0, 0)
    vehicle = Vehicle(width/2+10, height/2+10, velocity)
    food = Food(random(0,640),random(0,360),PVector(0,0))
    drawGraph()
    path = bfs(((vehicle.position[0])//20,(vehicle.position[1])//20), ((food.position[0])//20,(food.position[1])//20))


def draw():
    global path
    global stepCount
    
    drawGraph()
    updateWorld()
    draw_path()
    drawUI()
    #moveAgent(PVector(path[stepCount][0]*20+10,path[stepCount][1]*20+10))
    #vehicle.position = PVector(path[stepCount][0]*20+10,path[stepCount][1]*20+10)
    if (((vehicle.position[0])//20,(vehicle.position[1])//20) == (path[stepCount][0],path[stepCount][1]) and stepCount < len(path)-1):
        stepCount+=1
    if ((vehicle.position[0])//20,(vehicle.position[1])//20) == ((food.position[0])//20,(food.position[1])//20):
        resetFood()
        path = bfs(((vehicle.position[0])//20,(vehicle.position[1])//20), ((food.position[0])//20,(food.position[1])//20))
        stepCount = 0


def drawUI():
    #background(255)
    fill(50)
    text(str(foodCount),40,40,30,30)
    
def updateWorld():
    global path
    global stepCount
    vehicle.arrive(PVector(path[stepCount][0]*20+10,path[stepCount][1]*20+10))
    vehicle.update()
    vehicle.display()
    food.update()
    food.display()

def resetFood():
    global foodCount
    foodCount+=1
    food.position = PVector(random(0,width),random(0,height))

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
                
    current = goal 
    path = []
    while current != start: 
        path.append(current)
        stroke(0,255,0)
        
        line(current[0]*20+10,current[1]*20+10,came_from[current][0]*20+10,came_from[current][1]*20+10)
        current = came_from[current]
    path.append(start) # optional
    path.reverse() # optional
    return path

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
        print(type(n))
        print(type(n[0]))
        print(mapa)
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
            x = noise(xoff,yoff)*255
            if x < 63:
                cost = 1
                fill(68,150,90) #custo baixo caminhar na grama
            elif x < 126:
                cost = 5
                fill(150,75,0) #custo elevado caminhar na areia
            elif x < 189:
                cost = 10
                fill(18,10,143) #custo medio caminhar na agua
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
    
