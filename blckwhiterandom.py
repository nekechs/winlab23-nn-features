import pygame
import numpy as np
import os

# Adjust the probability of getting white screen (in percentage)
white_prob = 100
#for bee sim capure frame
frame_number = 0
frames_dir="frames"

# Initialize Pygame
pygame.init()

# Set the width and height of the screen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Random Screen Color")

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Set the total run time in seconds
total_time = 10
start_time = pygame.time.get_ticks()



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

    # Determine screen color based on the probability
    random_num = np.random.randint(1, 101)  # Generate a random integer between 1 and 100
    print(random_num)
    if random_num <= white_prob:
        screen.fill(pygame.Color("white"))
    else:
        screen.fill(pygame.Color("black"))

    # Update the screen
    pygame.display.flip()

    # Control the frame rate
    clock.tick(15)
    #-cpied from mayank's beesim
    frame_filename = os.path.join(frames_dir, f"frame_{frame_number:06d}.png")
    pygame.image.save(screen, frame_filename)
    frame_number += 1

# Quit the game
pygame.quit()