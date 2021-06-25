from Vehicle import Vehicle

def setup():
    global vehicle
    size(640, 360)
    velocity = PVector(0,0)
    vehicle = Vehicle(width/2,height/2,velocity)
    
def draw():
    background(255)
    mouse = PVector(mouseX,mouseY)
    vehicle.update()
    vehicle.display()
    
def keyTyped():
    if key == 'a':
        vehicle.applyForce(PVector(-1,0))
    if key == 'd':
        vehicle.applyForce(PVector(1,0))
    if key == 'w':
        vehicle.applyForce(PVector(0,-1))
    if key == 's':
        vehicle.applyForce(PVector(0,1))
