import pygame
import numpy as np
import random
import math
import time
import bee

# In this function, there is a 3 percent chance that we will turn CW by 0.1 radians.
def update_custom(instance):
    prob = 0.03
    if random.random() < prob:
        instance.rot += 0.1

x_width = 500
y_width = 500

pygame.init()

font = pygame.font.SysFont(None, 30)# for fps

# Set up the drawing window
screen = pygame.display.set_mode([x_width, y_width])

# Get the current time
start_time = time.time()
clock = pygame.time.Clock()

bees = []
for i in range(1):
    bees.append(bee.Bee(screen, 2, 0.15, custom_update=update_custom))

# Run the simulation for 2 minutes (120 seconds)
while time.time() - start_time < 120:
    #selecting the framerate
    clock.tick(60)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    start_frame_time = time.time()# for pygame fps
    # Fill the background with white
    screen.fill((255, 255, 255))

    for bee in bees:
        bee.update()
        bee.draw()
    
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, (0, 0, 0))
    screen.blit(fps_text, (10, 10))


    # Update the display
    pygame.display.flip()
    

# End the program after 2 minutes
pygame.quit()