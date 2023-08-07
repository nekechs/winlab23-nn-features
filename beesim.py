import pygame
import time
from bee import Bee, PathBee
import os
import subprocess
from datetime import datetime
import math

def bias_north(bee: Bee, bias):
    print(bee.rot)
    if bee.rot < 180:
        bee.rot -= int(bias)
    else:
        bee.rot += int(bias)

def test_pathbee():
    (x_dim, y_dim) = (1024, 1024)
    pygame.init()
    screen = pygame.display.set_mode([x_dim, y_dim])
    start_time = time.time()
    clock = pygame.time.Clock()

    # bee = PathBee(screen, 5.0, 20)
    bees = []
    for _ in range(1):
        # bees.append(PathBee(screen, 10, 20))
        bees.append(Bee(screen, walk_strength=2.0, custom_update=bias_north, dot_radius=20))
    for frame_number in range(1024):
        clock.tick(1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill((255, 255, 255))
        for (i, bee) in enumerate(bees):
            # bias = 0 if i < 5 else 90
            bias = 15
            bee.update(bias)
            bee.draw()

        pygame.display.flip()

test_pathbee()

# Combines all images from the "frames" directory into one video using ffmpeg
# def assemble_video(filename, frames_dir="frames", video_dir="videos"):
#     if not os.path.exists(video_dir):
#         os.makedirs(video_dir)
#     for f in os.listdir(video_dir):
#         os.remove(os.path.join(video_dir, f))

#     outfile_path = os.path.join(video_dir, f"{filename}.h264")
#     subprocess.call(["ffmpeg", "-r", "30", "-i", f"{frames_dir}/frame_%06d.png", "-c:v", "libx264", "-vf", "fps=60", outfile_path])
#     return outfile_path

# def make_frames(outfile, classnum, screen_dim, num_bees=1, fwd_amount=2, frames_dir="frames", video_dir="videos"):
#         # Initialize some pygame stuff
#     (x_dim, y_dim) = screen_dim
#     pygame.init()
#     font = pygame.font.SysFont(None, 30)
#     screen = pygame.display.set_mode([x_dim, y_dim])
#     start_time = time.time()
#     clock = pygame.time.Clock()

#     if not os.path.exists(frames_dir):
#         os.makedirs(frames_dir)
#     for f in os.listdir(frames_dir):
#         os.remove(os.path.join(frames_dir, f))
    
#     bees=[]
#     for i in range(num_bees):
#         bees.append(Bee(screen, fwd_amount, x_width=x_dim, y_width=y_dim))
    
#     frame_number = 0
#     while frame_number < 1024:  # Each of these is a frame
#         # clock.tick(120)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 exit()

#         start_frame_time = time.time()
#         screen.fill((255, 255, 255))
#         for bee in bees:
#             bee.update()
#             bee.draw()
        
#         fps = int(clock.get_fps())
#         fps_text = font.render(f"FPS: {fps}", True, (0, 0, 0))

#         # Display stuff - Save images
#         pygame.display.flip()
#         frame_filename = os.path.join(frames_dir, f"frame_{frame_number:06d}.png")
#         pygame.image.save(screen, frame_filename)
#         frame_number += 1
    
#     pygame.quit()