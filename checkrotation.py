import pygame
import numpy as np
import os
import beesim
from datetime import datetime
timestamp = datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S_%f')
metastamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
metastamp2 = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

frame_number = 0
frames_dir="frames"
class_dir="class"
metadata_dir="metadata"

pygame.init()

# Set the width and height of the screen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
screen.fill((255, 255, 255))
pygame.display.set_caption("circle rotation")

# Create a surface to draw the circle on
image_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
pygame.draw.circle(image_surface, (0, 0, 0), (100, 100), 100,False,True,True,True)

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Set the total run time in seconds
total_time = 10
start_time = pygame.time.get_ticks()

rotation_angle = 0
rotation_speed = 60

running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculate the elapsed time
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) / 1000  # Convert to seconds

    if elapsed_time >= total_time:
        running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    rotation_angle += rotation_speed * clock.get_time() / 1000

    # Rotate and draw the image
    rotated_image = pygame.transform.rotate(image_surface, rotation_angle)
    rotated_rect = rotated_image.get_rect(center=(400, 300))  # Center the rotated image
    screen.blit(rotated_image, rotated_rect)

    pygame.display.flip()

    # Control the frame rate
    clock.tick(30)

    classnum = 2
    frame_filename = os.path.join(frames_dir, f"{timestamp}_h264_{frame_number}.0.png")

    class_filename = os.path.join(class_dir, f"{timestamp}_h264_{frame_number}.cls")
    with open(class_filename, 'w') as file:
            file.write(f"{classnum}")

    metadata_filename = os.path.join(metadata_dir, f"{timestamp}_h264_{frame_number}.metadata.txt")
    with open(metadata_filename, 'w') as file:
            file.write(f"FAKEPATH/{metastamp}.h264,{frame_number},{metastamp2}")

    pygame.image.save(screen, frame_filename)
    frame_number += 1   