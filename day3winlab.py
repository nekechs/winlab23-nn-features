import pygame
import random
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
rotation_speed = 0.07  # Adjust the rotation speed to your liking

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

    # Generate random x and y velocities for dot movement
    x_velocity = random.uniform(-dot_speed, dot_speed)
    y_velocity = random.uniform(-dot_speed, dot_speed)

    # Update dot position based on velocities
    dot_x = max(dot_radius, min(dot_x + x_velocity, 500 - dot_radius))
    dot_y = max(dot_radius, min(dot_y + y_velocity, 500 - dot_radius))

    # Update rotation angle
    rotation_angle += rotation_speed

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
        rotated_point = pygame.math.Vector2(point).rotate(rotation_angle)
        rotated_arrow_points.append((rotated_point.x + dot_x, rotated_point.y + dot_y))

    pygame.draw.polygon(screen, arrow_color, rotated_arrow_points)

    # Update the display
    pygame.display.flip()

# End the program after 2 minutes
pygame.quit()