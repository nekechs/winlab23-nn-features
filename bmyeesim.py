import pygame
import numpy as np
import random
import math
import time

class DotSimulation:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode([width, height])
        self.dot_radius = 20
        self.dot_color = (255, 0, 0)
        self.dot_speed = 2
        self.dot_x = random.randint(self.dot_radius, width - self.dot_radius)
        self.dot_y = random.randint(self.dot_radius, height - self.dot_radius)
        self.rotation_angle = 0
        self.start_time = time.time()

    def run(self, duration):
        while time.time() - self.start_time < duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.update_dot_position()
            self.draw_dot()
            self.draw_arrow()
            pygame.display.flip()

        pygame.quit()

    def update_dot_position(self):
        forward_deviation = 4 * np.random.power(0.01)
        angle_deviation = np.random.normal(0, 0.03)
        x_deviation = forward_deviation * math.cos(self.rotation_angle)
        y_deviation = forward_deviation * math.sin(self.rotation_angle)
        self.rotation_angle += angle_deviation
        self.dot_x = max(self.dot_radius, min(self.dot_x + x_deviation, 500 - self.dot_radius))
        self.dot_y = max(self.dot_radius, min(self.dot_y + y_deviation, 500 - self.dot_radius))

    def draw_dot(self):
        self.screen.fill((255, 255, 255))
        pygame.draw.circle(self.screen, self.dot_color, (int(self.dot_x), int(self.dot_y)), self.dot_radius)

    def draw_arrow(self):
        arrow_color = (255, 255, 0)
        arrow_points = [
            (-10, 0),
            (10, 0),
            (0, -20),
            (-10, 0)
        ]
        rotated_arrow_points = []
        for point in arrow_points:
            rotated_point = pygame.math.Vector2(point).rotate_rad(self.rotation_angle + (math.pi / 2))
            rotated_arrow_points.append((rotated_point.x + self.dot_x, rotated_point.y + self.dot_y))

        pygame.draw.polygon(self.screen, arrow_color, rotated_arrow_points)

if __name__ == '__main__':
    simulation = DotSimulation(500, 500)
    simulation.run(120)