import pygame
import numpy as np

from bee import Bee
from make_dataset import Simulator

class BeeSimulator(Simulator):
    def __init__(self, screen: pygame.surface.Surface, bias_amt):
        self.screen = screen
        self.bee = Bee(screen, walk_strength=2, custom_update=None, dot_radius=20)

    def update(self):
        self.bee.update()
    
    def reset(self):
        self.bee.reset()

    def draw(self):
        self.bee.draw()

class LeftRightSimulator(Simulator):
    def __init__(self, screen: pygame.surface.Surface, bias_amt):
        (self.x_dim, self.y_dim) = screen.get_size()
        self.pos = (self.x_dim // 2, self.y_dim // 2)
        self.bias_amt = bias_amt

        self.angle = 0
        self.reset()
    
        # Pygame specific details
        self.radius = 128
        self.circlesurf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.circlesurf, (0, 0, 0), (self.radius, self.radius), self.radius, False, True, True, True)
        # pygame.init()
        self.screen = screen

        # Based on the current angle, draw the pacman onto the screen
    def draw_pacman_angle(self):
        rot_surf = pygame.transform.rotate(self.circlesurf, self.angle)
        rot_rect = rot_surf.get_rect(center=self.pos)
        self.screen.blit(rot_surf, rot_rect)

    def draw(self):
        self.screen.fill((255, 255, 255))
        # draw_pacman_angle(self.screen, self.pos[0], self.pos[1], self.angle)
        self.draw_pacman_angle()

    # Randomly resets the state of the simulation
    def reset(self):
        self.angle = np.random.rand(1,) * 360

    def update(self, classnum):
        delta_angle = np.random.uniform(1, 5)
        delta_angle = -delta_angle if classnum == 1 else delta_angle
        self.angle += delta_angle

class PacmanSimulator(Simulator):
    def __init__(self, screen: pygame.surface.Surface, bias_amt):
        # Parameters of the simulation that stay the same
        (self.x_dim, self.y_dim) = screen.get_size()
        self.pos = (self.x_dim // 2, self.y_dim // 2)
        self.bias_amt = bias_amt

        # Parameters of the simulation that get randomized
        self.angle = 0
        self.reset()
 
        # Pygame specific details
        self.radius = 128
        self.circlesurf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.circlesurf, (0, 0, 0), (self.radius, self.radius), self.radius, False, True, True, True)
        # pygame.init()
        self.screen = screen

    # Based on the current angle, draw the pacman onto the screen
    def draw_pacman_angle(self):
        rot_surf = pygame.transform.rotate(self.circlesurf, self.angle)
        rot_rect = rot_surf.get_rect(center=self.pos)
        self.screen.blit(rot_surf, rot_rect)

    def draw(self):
        self.screen.fill((255, 255, 255))
        # draw_pacman_angle(self.screen, self.pos[0], self.pos[1], self.angle)
        self.draw_pacman_angle()

    # Randomly resets the state of the simulation
    def reset(self):
        self.angle = np.random.rand(1,) * 360
    
    # This function advances the timestep by 1
    # Classnum 1 - random; classnum 2 - non random
    def update(self, classnum):
        bias = 0 if classnum == 1 else self.bias_amt
        # delta_angle = np.random.uniform(-10, 10)
        if np.random.rand(1,) < 0.5:
            delta_angle = -(np.random.rand(1,) * 4 + 1)
            pass
        else:
            delta_angle = (np.random.rand(1,) * 4 + 1) + bias
            delta_angle += bias
        self.angle += delta_angle

class BWSimulator(Simulator):
    def __init__(self, screen: pygame.surface.Surface, bias_amt):
        # Params of simulation that stay the same
        self.x_dim, self.y_dim = screen.get_size()
        self.bias_amt = bias_amt

        # Parameters of the simulation subject to change
        self.brightness = 0.0
        
        # Pygame specific details
        self.screen = screen

    def draw(self):
        self.screen.fill((self.brightness * 255, self.brightness * 255, self.brightness * 255))

    def reset(self):
        self.brightness = 0.0

    def update(self, classnum):
        self.brightness = 0.0 if classnum == 1 else 1.0
