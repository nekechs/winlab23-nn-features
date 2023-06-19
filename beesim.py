import pygame
import numpy as np
import random
import math
import time
import bee
import os
import subprocess

# setup for video extraction
frames_dir = "frames"
if not os.path.exists(frames_dir):
    os.makedirs(frames_dir)
for f in os.listdir(frames_dir):
    os.remove(os.path.join(frames_dir, f))

# In this function, there is a 3 percent chance that we will turn CW by 0.1 radians.
def update_custom(instance):
    prob = 0.3
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

frame_number=0
while frame_number < 10000:
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
    # screen.blit(fps_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Save the current frame as an image on disk
    frame_filename = os.path.join(frames_dir, f"frame_{frame_number:06d}.png")
    pygame.image.save(screen, frame_filename)

    frame_number += 1

# End the program
pygame.quit()

output_filename = "output.h264"
subprocess.call(["ffmpeg", "-r", "30", "-i", f"{frames_dir}/frame_%06d.png", "-c:v", "libx264", "-vf", "fps=60", output_filename])