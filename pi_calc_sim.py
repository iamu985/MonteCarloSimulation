import random
import pygame
from math import sqrt
import config as c
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

class Simulate:
    def __init__ (self, epoch):
        self.size = c.size
        self.fps = c.fps
        self.bg = c.bgcolor
        self.circleradius = c.circleradius
        self.circlecolor = c.circlecolor
        self.circlecenter = c.circlecenter
        self.rball = c.rball
        self.ballcolor = c.ballcolor
        self.clock = pygame.time.Clock()
        self.values_pi = [0]
        self.epoch = epoch
        self.circle = 0
        self.square = 0
        self.xgenerations = [0]

    def draw_balls(self, surface):
        #generates random balls and returns the position of the balls
        center = (random.randint(0, 801), random.randint(0, 801))
        pygame.draw.circle(surface, self.ballcolor, center, self.rball)
        return center

    def check_balls(self, ball_pos):
        distance = sqrt((ball_pos[0]-self.circleradius)**2+(ball_pos[1]-self.circleradius)**2)
        if distance < self.circleradius:
            self.circle += 1
            self.square += 1
        if distance > self.circleradius:
            self.square += 1
        return self.square, self.circle
    
    def __call__(self):
        pygame.init()
        call = Simulate(self.epoch)
        surface = pygame.display.set_mode(self.size)
        run_simulation = True
        surface.fill(self.bg)
        generation = 0
        #displaying text
        font = pygame.font.Font('freesansbold.ttf', 24)
        while run_simulation:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    run_simulation = False
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        run_simulation = False
                    if ev.key == pygame.K_q:
                        run_simulation = False
            
            pygame.draw.circle(surface, self.circlecolor, self.circlecenter, self.circleradius, 2)
            
            #drawing balls
            if generation < self.epoch:
                ball_position = call.draw_balls(surface)
                s, c = call.check_balls(ball_position)

                try:
                    estimated_pi = 4*c/s
                except ZeroDivisionError:
                    estimated_pi = 0
                self.values_pi.append(estimated_pi)
                generation+=1
                self.xgenerations.append(generation)
                if generation % 10 == 0:
                    print(f'GENERATION: {generation}, Balls Generated: {s}, Balls inside Circle: {c}')
                    
                text = font.render(f'Estimated Value of Pi {estimated_pi}', True, (221, 0, 0), (221, 221, 221))
                textrect = text.get_rect()
                textrect.x = 175
                textrect.y = 10
                surface.blit(text, textrect)

            pygame.display.update()
            self.clock.tick(self.fps)
            
        def animate(i):
            plt.cla()
            plt.plot(self.xgenerations, self.values_pi)
                
        animate = FuncAnimation(plt.gcf(), animate, interval=10000)
        plt.tight_layout()
        plt.show()
            
        pygame.quit()
        


if __name__ == '__main__':
    test_size = int(input('Test Size: '))
    simulate = Simulate(test_size)
    simulate()
    

            
            
        
            
