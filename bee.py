import numpy as np
import pygame
import math
import random

class Bee:
    def __init__(self, screen: pygame.surface.Surface, walk_strength, custom_update=None, dot_radius=20):
        # Initialize the screen parameters
        self.screen = screen
        (self.x_width, self.y_width) = screen.get_size()

        # Initialize position and rotation
        self.x_pos = random.uniform(0,self.x_width)
        self.y_pos = random.uniform(0,self.y_width)
        self.rot = 2 * math.pi * random.random()
        self.reset()

        self.dot_radius = dot_radius
        self.dot_color = (255, 0, 0)

        self.walk_strength = walk_strength

        # Stuff stored to make the arrow
        self.arrow_color = (255, 255, 0)
        self.arrow_points = [
            (-10, 0),
            (10, 0),
            (0, -20),
            (-10, 0)
        ]

        self.custom_update = custom_update

    def update(self):
        self.update_rand()
        self.update_nonrand()
    
    def update_rand(self):
        forward_deviation = self.walk_strength * int(10 * np.random.random())
        angle_deviation = (2 * math.pi / 360) * int(360 * np.random.random())

        # Deviation of x and y
        x_deviation = forward_deviation * math.cos(self.rot)
        y_deviation = forward_deviation * math.sin(self.rot)

        self.rot = angle_deviation

        # Update dot position
        self.x_pos = max(self.dot_radius, min(self.x_pos + x_deviation, self.x_width - self.dot_radius))
        self.y_pos = max(self.dot_radius, min(self.y_pos + y_deviation, self.y_width - self.dot_radius))

    def update_nonrand(self):
        if self.custom_update is not None:
            return self.custom_update(self)

    def reset(self):
        # Initialize position and rotation
        self.x_pos = random.uniform(0,self.x_width)
        self.y_pos = random.uniform(0,self.y_width)
        self.rot = 2 * math.pi * random.random()

    def draw(self):
        # Draw the circle
        pygame.draw.circle(self.screen, self.dot_color, (int(self.x_pos), int(self.y_pos)), self.dot_radius)
        
        # Draw the triangle
        rotated_arrow_points = []
        for point in self.arrow_points:
            rotated_point = pygame.math.Vector2(point).rotate_rad(self.rot + (math.pi / 2))
            rotated_arrow_points.append((rotated_point.x + self.x_pos, rotated_point.y + self.y_pos))
        pygame.draw.polygon(self.screen, self.arrow_color, rotated_arrow_points)