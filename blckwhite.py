import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Set the width and height of the screen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Random Screen Color")

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Set the total run time in seconds
total_time = 120
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

    # Generate a random number using NumPy
    random_num = np.random.randint(1, 3)  # Generate a random integer between 1 and 2
    #print(random_num)

    # Determine screen color based on the random number
    if random_num == 1:
        screen.fill(pygame.Color("white"))
    else:
        screen.fill(pygame.Color("black"))

    # Update the screen
    pygame.display.flip()

    # Control the frame rate
    clock.tick(15)

# Quit the game
pygame.quit()