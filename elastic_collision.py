import pygame, random 
import numpy as np
import pygame.gfxdraw

# detect collision and change velocity
class Environment():
    def __init__(self, DIM, dt):
        self.DIM = DIM
        self.dt = dt
        self.particles = []

    def update(self):
        for p1 in self.particles:
            p1.stateUpdate()
            self.bounce(p1)
            for p2 in self.particles:
                if p1 != p2:
                    self.elasticCollision(p1, p2)

    def addParticle(self, p):
        self.particles.append(p)

    # collision between particle and extremity
    def bounce(self, p):
        for p in self.particles:
            i = 0
            for x in p.X[0]:
                if x > self.DIM[i]-p.radius:
                    dist = p.radius-(self.DIM[i]-x)
                    p.addPosition(-dist)
                    tmp = np.zeros(np.size(p.V))
                    tmp[i] = -2*p.V[0][i]
                    p.addVelocity(tmp)
                elif x < p.radius: 
                    dist = p.radius-x
                    p.addPosition(dist)
                    tmp = np.zeros(np.size(p.X))
                    tmp[i] = -2*p.V[0][i]
                    p.addVelocity(tmp)
                i += 1
    # collision between particle and particle
    def elasticCollision(self, p1, p2):
        dX = p1.X-p2.X
        dist = np.sqrt(np.sum(dX**2))
        if dist < p1.radius+p2.radius:
            offset = dist-(p1.radius+p2.radius)
            p1.addPosition((-dX/dist)*offset/2)
            p2.addPosition((dX/dist)*offset/2)
            total_mass = p1.mass+p2.mass
            dv1 = -2*p2.mass/total_mass*np.inner(p1.V-p2.V,p1.X-p2.X)/np.sum((p1.X-p2.X)**2)*(p1.X-p2.X)
            dv2 = -2*p1.mass/total_mass*np.inner(p2.V-p1.V,p2.X-p1.X)/np.sum((p2.X-p1.X)**2)*(p2.X-p1.X)
            p1.addVelocity(dv1)
            p2.addVelocity(dv2)

    def plasticCollision(self):
        pass

# updade particle position and velocity
class Particle():
    def __init__(self, env, X, V,radius, mass):
        self.env = env
        self.X = X
        self.V = V
        self.radius = radius
        self.mass = mass
        self.colour = (0, 0, int(random.uniform(0,255)))

    def addVelocity(self, vel):
        self.V += vel
    
    def addPosition(self, pos):
        self.X += pos

    def stateUpdate(self): 
        self.X += self.V*self.env.dt

# simulation startup
DIM = np.asarray([700, 700])
dt = 0.01
env = Environment(DIM, dt)

pygame.init()
screen = pygame.display.set_mode((DIM[0], DIM[1]))
pygame.display.set_caption('Simulador de colisões elásticas')
number_of_particles= 50

# particles parameters, X(position), V(velocity)

for n in range(number_of_particles):
    radius = np.random.randint(10, 20)
    mass = radius**3
    X = np.random.rand(1, 2)*(DIM-radius)+radius
    V = np.random.rand(1, 2)*75
    particle = Particle(env, X, V, radius, mass)
    env.addParticle(particle)

def display(env):
    for p in env.particles:
        pygame.gfxdraw.filled_circle(screen, int(p.X[0][0]), int(p.X[0][1]), p.radius, p.colour)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill([255, 255, 255])
    env.update()
    display(env)
    pygame.display.flip()