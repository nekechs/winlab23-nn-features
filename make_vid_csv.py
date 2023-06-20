import pygame
import numpy as np
import random
import time
from bee import Bee
import os
import subprocess
import csv

videos_dir="videos/first-set"

# Some probability of turning right by 0.1 radians
def update_custom(instance):
    prob = 0.03
    if random.random() < prob:
        instance.rot += 0.1

def generate_video(outfile, num_bees, fwd_amount, turn_amount, is_fullrand, screen_dim=(512, 512), video_dir=videos_dir):
    # setup frames directory
    frames_dir="frames"
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)
    if not os.path.exists(video_dir):
        os.makedirs(video_dir)
    for f in os.listdir(frames_dir):
        os.remove(os.path.join(frames_dir, f))
    
    # Initialize some pygame stuff
    (x_width, y_width) = screen_dim
    pygame.init()
    font = pygame.font.SysFont(None, 30)
    screen = pygame.display.set_mode([x_width, y_width])
    start_time = time.time()
    clock = pygame.time.Clock()

    bees=[]
    for i in range(num_bees):
        bees.append(Bee(screen, fwd_amount, turn_amount, x_width=x_width, y_width=y_width))
    
    frame_number = 0
    while frame_number < 1024:  # Each of these is a frame
        # clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        start_frame_time = time.time()
        screen.fill((255, 255, 255))
        for bee in bees:
            bee.update()
            bee.draw()
        
        fps = int(clock.get_fps())
        fps_text = font.render(f"FPS: {fps}", True, (0, 0, 0))

        # Display stuff - Save images
        pygame.display.flip()
        frame_filename = os.path.join(frames_dir, f"frame_{frame_number:06d}.png")
        pygame.image.save(screen, frame_filename)

        frame_number += 1
    
    pygame.quit()
    output_file = f"{os.path.join(video_dir, outfile)}.h264"
    subprocess.call(["ffmpeg", "-r", "30", "-i", f"{frames_dir}/frame_%06d.png", "-c:v", "libx264", "-vf", "fps=60", output_file])
    return output_file

for f in os.listdir(videos_dir):
    os.remove(os.path.join(videos_dir, f))

with open("dataset.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    field = ["file", "class", "begin frame", "end frame"]
    writer.writerow(field)
    num_videos = 150
    for video_number in range(num_videos):
        if random.random() < 0.5:
            file = generate_video(f"sample{video_number}", 1, 2, 0.15, True)
            nn_class=1
        else:
            file = generate_video(f"sample{video_number}", 1, 2, 0.15, False)
            nn_class=2
        writer.writerow([os.path.abspath(file), nn_class, 50, 1000])
