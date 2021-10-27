# Import libraries
import pygame, sys, random, math
from pygame import gfxdraw

C = pygame.time.Clock() # Clock

from pygame.locals import *
pygame.init() # Initiate pygame

pygame.font.init() # Initialise font package

pygame.display.set_caption("Pong: Richard Edition")

WS = (800, 600) # Tuple encapsulating screen size parameters

colA = {"WHITE": (255, 255, 255), "BLACK": (0, 0, 0), "RED": (192, 57, 43)} # Dictionary encapsulating colour RGB correspondences

FPS = 60 # Frames per second parameter

S = pygame.display.set_mode(WS) # Generate screen object and assign dimension parameters

def rectangle(self, surface, points, color):
    '''Render anti-alised rectangle'''

    gfxdraw.aapolygon(surface, points, color)
    gfxdraw.filled_polygon(surface, points, color)

class Particle():
    '''Particle class encoding physical parameters and methods of propagation, boundary conditions and reset'''
    def __init__(self, l, vo, o = [WS[0]/2, WS[1]/2]):
        self.l = l # Length
        self.ivo = vo # Initial Velocity
        self.vo = vo # Velocity
        thetao = random.randrange(-60, 60) # Angle Theta
        self.coord = [o[0], o[1]] # Center Coordinates
        self.io = [WS[0]/2, WS[1]/2] # Initial Origin
        self.delay = False # Delay Boolean
        #
        # self.theta = random.randrange(-60, 60)
        self.vy = math.sin(math.radians(thetao))*vo # Y axis velocity composition
        self.vx = math.cos(math.radians(thetao))*vo # X axis velocity composition
        self.R = pygame.Rect(o[0]-l/2, o[1]-l/2, l, l) # Definition of Rectangle Object
        #self.thetaR = math.radians(self.theta)

        #self.vx = math.cos(self.thetaR) * self.v
        #self.vy = math.sin(self.thetaR) * self.v



    '''def resolve(self):
        self.thetaR = math.radians(self.theta)
        self.vx = math.cos(self.theta) * self.v
        self.vy = math.sin(self.theta) * self.v'''

    def propagate(self):
        #self.resolve()
        self.coord[0] = self.coord[0] + self.vx # Eulerian Kinematic Integration - X-Axis
        self.coord[1] = self.coord[1] + self.vy # Eulerian Kinematic Integration - Y-Axis

        self.R = pygame.Rect(self.coord[0]-self.l/2, self.coord[1]-self.l/2, self.l, self.l) # Redefine Rectangle Object
    
    def boundary(self):
        #if self.coord[0]+self.l/2 >= WS[0]:
            #self.coord[0] = WS[0]-self.l/2
            #self.theta = 180-self.theta
            #self.vx = -self.vx
        #elif self.coord[0]-self.l/2 <= 0:
            #self.coord[0] = self.l/2
            #self.vx = -self.vx
            #self.theta = 180-self.theta
        if self.coord[1]+self.l/2 >= WS[1]: # Invert vertical velocity if particle coordinate surpasses upper boundary.
            self.coord[1] = WS[1]-self.l/2
            self.vy = -self.vy
            #self.theta = -self.theta
        elif self.coord[1]-self.l/2 <= 0: # Invert vertical velocity if particle coordinate surpasses lower boundary
            self.coord[1] = self.l/2
            self.vy = -self.vy
            #self.theta = -self.theta

    def Render(self):
        if self.delay == False:
            self.propagate() # Recompute particle kinematic coordinates
            self.boundary() # Execute boundary conditions
        pygame.draw.rect(S, colA["RED"], self.R) # Render particle object

    def Reset(self):
        self.coord[0] = self.io[0] # Reset particle x coordinate to origin
        self.coord[1] = self.io[1] # Reset particle y coordinate to origin

        self.R = pygame.Rect(self.coord[0]-self.l/2, self.coord[1]-self.l/2, self.l, self.l) # Redefine rectangle object

        thetao = random.randrange(-60, 60) # Assign random theta from -60 to 60 to origin theta

        self.vy = math.sin(math.radians(thetao))*self.ivo # Recompute component velocity
        self.vx = math.cos(math.radians(thetao))*self.ivo # Recompute component velocity
        
        self.vo = self.ivo # Reset velocity magnitude to initial magnitude

        self.delay = True # Delay for period defined in main loop

class PYPaddle():
    '''Foundational Player Paddle Class encapsulating physical paramters and methods enabling dynamic interaction, movement of Paddle'''
    def __init__(self, h, l, a, vo, o=[WS[0]-20, WS[1]/2]):
        self.o = [o[0], o[1]] # Origin Coordinates
        self.R = pygame.Rect(o[0]-h/2, o[1]-l/2, h, l)  # Define Rectangle Object
        self.a = a # Acceleration
        self.ia = a # Initial Acceleration
        self.D = 0.1 # Drag Force
        self.vo = vo # Initial Velocity
        self.h = h # Height
        self.l = l # Length
        self.nt = pygame.time.get_ticks() # New Time
        self.pt = 0 # Previous Time
        self.dt = 20 # Delta Time
    
    def Up(self):
        self.vo = self.vo - self.a # Exert Upward Force: Eulerian acceleration integration

    def Down(self):
        self.vo = self.vo + self.a # Exert Downard Force: Euleriean acceleration integration
    
    def Boundary(self):
        if self.o[1] - self.l/2 <= 0: # Apply boundary conditions
            self.o = WS[0]-20, self.l/2 
            self.vo = 0
        elif self.o[1] + self.l/2 >= WS[1]:
            self.o = WS[0]-20, WS[1] - self.l/2
            self.vo = 0

    def Propagate(self):
        if self.nt >= self.pt + self.dt:
            if self.vo > 0:
                self.vo = self.vo - self.D # Perpetual Drag Force Diminishing Velocity
            else:
                self.vo = self.vo + self.D # Perpetual Drag Force Diminishing Velocity
            if abs(self.vo) < 0.15:
                self.vo = 0 # Nullify Velocity 
            
            self.pt = self.nt
        self.o = self.o[0], self.o[1] + self.vo # Recompute Coordinate Parameters
        self.nt = pygame.time.get_ticks()
    
    def Render(self):
        self.Propagate() # Propagate Particle
        self.Boundary() # Apply Boundary Conditions
        self.R = pygame.Rect(self.o[0]-self.h/2, self.o[1]-self.l/2, self.h, self.l) # Define Rectangle Object
        pygame.draw.rect(S, colA["WHITE"], self.R) # Render Player Paddle

class AIPaddle(PYPaddle): # Inherit From Parent PyPaddle Class
    def __init__(self, Er, Tx, a, l):
        super().__init__(10, l, a, 0, o=[20, WS[1]/2]) # Initisalise Parent Class
        self.Eq = WS[1]/2 # Equillibrium Position
        self.Er = Er # Innaccuray Threshold
        self.Tx = Tx # X Threshold
        self.x = random.randrange(0, 21) # Random Innaccuracy Variable
        self.deflect = False # Boolean Flag Intiating Ball Trajectory Prediction

    def Boundary(self): # Check Boundary Conditions
        if self.o[1] - self.l/2 <= 0:
            self.o = 20, self.l/2 
            self.vo = 0
        elif self.o[1] + self.l/2 >= WS[1]:
            self.o = 20, WS[1] - self.l/2
            self.vo = 0
    
    def InterceptCoord(self, vx, vy, coord): # Predict Ball Trajectory Intercept
        nvx = vx 
        nvy = vy
        ncoord = coord.copy()

        while ncoord[0] > self.o[0]:
            ncoord[0] = ncoord[0] + nvx
            ncoord[1] = ncoord[1] + nvy

            if ncoord[1]+self.l/2 >= WS[1]:
                ncoord[1] = WS[1]-self.l/2
                nvy = -nvy
                #self.theta = -self.theta
            elif ncoord[1]-self.l/2 <= 0:
                ncoord[1] = self.l/2
                nvy = -nvy
                #self.theta = -self.theta
        return ncoord[1]
    
    def Converge(self, yp): # Converge To Argument Coordinates
        if self.o[1] > yp + 10:
            self.Up()
        elif self.o[1] < yp - 10:
            self.Down()
        elif abs(self.o[1] - yp) <= 10:
            self.vo = 0
        if abs(self.o[1] - yp) <= 15:
            self.a = self.a*abs(self.o[1] - yp)/15
        else:
            self.a = self.ia

    def Navigate(self, py): # Navigate To Particle Coordinates If Particle Propagating To AI Paddle; Else, Converge To Equillibrium
        if self.deflect == True:
            if self.o[0] <= self.Tx:
                print(self.x)
                if self.x == 5:
                    self.Converge(py-80)
                else:
                    self.Converge(py)
        else:
            self.Converge(self.Eq) 

def Collision(particle, paddle):
    r1 = paddle.R
    r2 = particle.R

    col = r1.colliderect(r2) # Ascertain Collision Boolean

    if col == True:

        s = particle.coord[1] - paddle.o[1] # Quantify Particle Displacement From Paddle Origin

        if particle.vx >= 0:
            theta = math.radians(180-(s / paddle.l/2 * 180)) # Compute Angle Theta In Accordance With Displacement Ratio: S

            particle.vx = math.cos(theta) * particle.vo # Velocity Composition
            particle.vy = math.sin(theta) * particle.vo
        else:
            
            theta = math.radians((s / paddle.l/2 * 180))

            particle.vx = math.cos(theta) * particle.vo
            particle.vy = math.sin(theta) * particle.vo
        
        paddle.x = random.randrange(0, 21) # Recompute Random Variable
    
    return col

pt = pygame.time.get_ticks()
nt = pygame.time.get_ticks()
dt = 1000
t_elapsed = 0

def Delay(t, particle): # Delay For t Seconds
    global t_elapsed
    global nt
    global pt
    global dt

    if t_elapsed < t/1000:
        if nt >= pt + dt:
            t_elapsed = t_elapsed + 1
            pt = nt
        nt = pygame.time.get_ticks()
    else:
        particle.delay = False   
    
          

P = Particle(10, 5) # Instantiate Particle Object
PaddleA = PYPaddle(10, 100, 1, 0) # Instantiate PYPaddle Object
PaddleB = AIPaddle(0.1, 100, 1.5, 100) # Instantaite AIPaddle Object

ScoreA = 0 # Score A Variable
ScoreB = 0 # Score B Variable

ColIter = 0 # Collision Iterations
PVMult = 1.05 # Particle Velocity Multiplier

itpcoord = 0 # Intercept Coordinate

while True:
    S.fill((41, 128, 185)) # Background Fill
    pygame.draw.line(S, colA["WHITE"], [WS[0]/2, 0], [WS[0]/2, WS[1]], 5)
    pygame.draw.line(S, colA["WHITE"], [0, 80], [WS[0], 80], 5)


    P.Render()
    PaddleA.Render()
    PaddleB.Render()

    #print("vx: " + str(P.vx))
    #print("vy: " + str(P.vy))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    keys = pygame.key.get_pressed() # Ascertain Key Press
    if keys[pygame.K_UP]:
        PaddleA.Up()
    if keys[pygame.K_DOWN]:
        PaddleA.Down() 
    
    
    if Collision(P, PaddleA) == True or Collision(P, PaddleB) == True: # Collision Computations
        ColIter = ColIter + 1 # Collision Iteration
        P.vo = P.vo * PVMult # Particle Velocity Multuplier
        
        #P.vx = P.vx * PVMult
        #P.vy = P.vy * PVMult
    
    if P.coord[0] > WS[0]: # Increment Score If Surpassed Right Bound
        ScoreA = ScoreA + 1
        P.Reset()
        t_elapsed = 0
    elif P.coord[0] < 0: # Increment Score If Surpassed Left Bound
        ScoreB = ScoreB + 1
        P.Reset()
        t_elapsed = 0
    
    if P.delay == True:
        F = pygame.font.SysFont("DroidSans", 120)
        t = F.render(str(t_elapsed+1), 1, (60, 60, 255))
        S.blit(t, (WS[0]/2-22.5,WS[1]/3))
    
    Delay(3000, P)

    nt = pygame.time.get_ticks()

    if P.vx < 0:
        PaddleB.deflect = True # Deflect Particle
        itpcoord = PaddleB.InterceptCoord(P.vx, P.vy, P.coord) # Evaluate Intercept Coordinate Of Particle With AIPaddle
    else:
        PaddleB.deflect = False

    PaddleB.Navigate(itpcoord)

    F = pygame.font.SysFont("DroidSans", 120) # Render Points
    t = F.render(str(ScoreA), 1, colA["WHITE"])
    S.blit(t, (WS[0]/6,0))
    t = F.render(str(ScoreB), 1, colA["WHITE"])
    S.blit(t, (5*WS[0]/6,0))

    #print(P.coord[0])

    pygame.display.flip()
    C.tick(FPS)
