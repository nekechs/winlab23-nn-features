import numpy as np
import pygame
import math
import random

POS_XAXIS = pygame.math.Vector2(1, 0)

class PathBee:
    def __init__(self, screen: pygame.surface.Surface, walk_strength, dot_radius = 20):
        # Initialize the screen parameters
        self.screen = screen
        (self.x_width, self.y_width) = screen.get_size()

        # Initialize position and rotation
        # self.start_pos = pygame.math.Vector2(np.random.uniform(0, self.x_width),
        #                                     np.random.uniform(0, self.y_width))
        # self.end_pos = pygame.math.Vector2(np.random.uniform(0, self.x_width),
        #                                     np.random.uniform(0, self.y_width))
        self.start_pos = pygame.math.Vector2(360, 200)
        self.end_pos = pygame.math.Vector2(250, 310)
        self.current_pos = pygame.math.Vector2(self.start_pos)
        self.rot = 2 * math.pi * random.random()
        # self.reset()

        goal_displacement = self.end_pos - self.start_pos
        self.Dmax = goal_displacement.length()

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

    def reset(self):
        self.start_pos = pygame.math.Vector2(np.random.uniform(0, self.x_width),
                                            np.random.uniform(0, self.y_width))
        self.end_pos = pygame.math.Vector2(np.random.uniform(0, self.x_width),
                                            np.random.uniform(0, self.y_width))
        self.current_pos = pygame.math.Vector2(self.start_pos)
        self.rot = 2 * math.pi * random.random()

    # F is the amount of field distortion.
    def update(self, F):
        goal_displacement = (self.end_pos - self.current_pos)
        dist = goal_displacement.length()
        if dist < self.dot_radius:
            return
        self.current_pos += POS_XAXIS.rotate(self.rot) * self.walk_strength
        direct_angle = POS_XAXIS.angle_to(goal_displacement)

        field_distortion = F * (1 - math.exp(- direct_angle**2))
        print(direct_angle ** 2)
        # field_distortion = F
        if direct_angle >= 0:
            J = min(360, direct_angle + field_distortion)
        else:
            direct_angle += 360
            J = max(0, direct_angle - field_distortion)

        # if direct_angle < 0:
        #     direct_angle += 360
        # if self.rot < 180:
        #     J = min(360, self.rot + F)
        # else:
        #     J = max(0, self.rot - F)

        # print(f"Direct angle: {direct_angle}; J: {J}")

        W1 = (dist - self.Dmax) ** 2 / (self.Dmax ** 2)
        W2 = 1 - W1
        self.rot = W1 * direct_angle + W2 * J
        # print(f"{self.rot}\n")

    def draw(self):
        # Draw the circle
        pygame.draw.circle(self.screen, self.dot_color, self.current_pos, self.dot_radius)
        pygame.draw.circle(self.screen, pygame.Color("blue"), self.start_pos, self.dot_radius)
        pygame.draw.circle(self.screen, pygame.Color("green"), self.end_pos, self.dot_radius)

        # Draw the triangle
        rotated_arrow_points = []
        for point in self.arrow_points:
            rotated_point = pygame.math.Vector2(point).rotate(self.rot + 90)
            rotated_arrow_points.append((rotated_point.x + self.current_pos.x, rotated_point.y + self.current_pos.y))
        pygame.draw.polygon(self.screen, self.arrow_color, rotated_arrow_points)

class Bee:
    def __init__(self, screen: pygame.surface.Surface, walk_strength, custom_update=None, dot_radius=20):
        # Initialize the screen parameters
        self.screen = screen
        (self.x_width, self.y_width) = screen.get_size()

        # Initialize position and rotation
        self.x_pos = 0
        self.y_pos = 0
        self.rot = 0
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

    def update(self, bias):
        self.update_rand()
        self.update_nonrand(bias)
    
    def update_rand(self):
        forward_deviation = self.walk_strength * int(10 * np.random.random())
        angle_deviation = int(360 * np.random.random())

        # Deviation of x and y
        x_deviation = forward_deviation * math.cos(self.rot / (180 / math.pi))
        y_deviation = forward_deviation * math.sin(self.rot / (180 / math.pi))

        self.rot = angle_deviation

        # Update dot position
        self.x_pos = max(self.dot_radius, min(self.x_pos + x_deviation, self.x_width - self.dot_radius))
        self.y_pos = max(self.dot_radius, min(self.y_pos + y_deviation, self.y_width - self.dot_radius))

    def update_nonrand(self, bias):
        if self.custom_update is not None:
            return self.custom_update(self, bias)

    def reset(self):
        # Initialize position and rotation
        self.x_pos = int(np.random.uniform(0,self.x_width))
        self.y_pos = int(np.random.uniform(0,self.y_width))
        self.rot = int(np.random.uniform(0, 360))

    def draw(self):
        # Draw the circle
        pygame.draw.circle(self.screen, self.dot_color, (self.x_pos, self.y_pos), self.dot_radius)
        
        # Draw the triangle
        rotated_arrow_points = []
        for point in self.arrow_points:
            rotated_point = pygame.math.Vector2(point).rotate(self.rot + 90)
            rotated_arrow_points.append((rotated_point.x + self.x_pos, rotated_point.y + self.y_pos))
        pygame.draw.polygon(self.screen, self.arrow_color, rotated_arrow_points)