import pygame
import numpy as np
import random
import math
import time

pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])

# Define dot properties
dot_radius = 20
dot_color = (255, 0, 0)
dot_speed = 2

# Initialize dot position
dot_x = random.randint(dot_radius, 500 - dot_radius)
dot_y = random.randint(dot_radius, 500 - dot_radius)

# Initialize dot rotation
rotation_angle = 0

# Get the current time
start_time = time.time()

# Run the simulation for 2 minutes (120 seconds)
while time.time() - start_time < 120:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Update angle and generate some new walk amount
    forward_deviation = 4 * np.random.power(0.01)
    angle_deviation = np.random.normal(0, 0.03)

    x_deviation = forward_deviation * math.cos(rotation_angle)
    y_deviation = forward_deviation * math.sin(rotation_angle)

    rotation_angle += angle_deviation

    # Update dot position based on velocities
    dot_x = max(dot_radius, min(dot_x + x_deviation, 500 - dot_radius))
    dot_y = max(dot_radius, min(dot_y + y_deviation, 500 - dot_radius))

    # Draw the dot on the screen
    pygame.draw.circle(screen, dot_color, (int(dot_x), int(dot_y)), dot_radius)

    # Draw an arrow inside the dot with rotation
    arrow_color = (255, 255, 0)
    arrow_points = [
        (-10, 0),
        (10, 0),
        (0, -20),
        (-10, 0)
    ]
    rotated_arrow_points = []
    for point in arrow_points:
        rotated_point = pygame.math.Vector2(point).rotate_rad(rotation_angle + (math.pi / 2))
        rotated_arrow_points.append((rotated_point.x + dot_x, rotated_point.y + dot_y))

    pygame.draw.polygon(screen, arrow_color, rotated_arrow_points)

    # Update the display
    pygame.display.flip()

# End the program after 2 minutes
pygame.quit()