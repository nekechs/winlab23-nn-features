import pygame
import numpy as np
import random
import math
import time
import bee

x_width = 500
y_width = 500

pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([x_width, y_width])

# Get the current time
start_time = time.time()
clock = pygame.time.Clock()

bees = []
for i in range(10):
    bees.append(bee.Bee(screen, 2, 0.15))

# Run the simulation for 2 minutes (120 seconds)
while time.time() - start_time < 120:
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Fill the background with white
    screen.fill((255, 255, 255))

    for bee in bees:
        bee.update()
        bee.draw()

    # Update the display
    pygame.display.flip()

# End the program after 2 minutes
pygame.quit()