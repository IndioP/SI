inc = 0.2
xoff = 0
yoff = 0

def setup():
    size(640,360)
    
def draw():
    
    drawGraph()
    
    
def drawGraph():
    global inc
    global xoff
    global yoff
    yoff = 0
    for j in range(10,height,20):
        xoff = 0
        for i in range(10,width,20):
            xoff+=inc
            x = noise(xoff,yoff)*255
            if x < 100:
                fill(68,150,90) #custo baixo caminhar na grama
            elif x < 170:
                fill(150,75,0) #custo elevado caminhar na areia
            else:
                fill(18,10,143) #custo medio caminhar na agua
            
            #print(x)
            #fill(x)
            stroke(0)
            square(i-10, j-10, 20)
            #fill(0,0,255)
            #circle(i, j, 3)
        yoff+=inc
