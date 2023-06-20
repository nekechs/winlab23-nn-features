import pygame
import numpy as np
import random
import time
from bee import Bee
import os
import subprocess
import csv
from datetime import datetime

# Create this command because we want to start a ffmpeg process and pipe frames to it
def prepare_ffmpeg_cmd(outfile, screen_dim=(512, 512)):
    (x_width, y_width) = screen_dim
    ffmpeg_command = [
        "ffmpeg",
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{x_width}x{y_width}",
        "-pix_fmt", "rgb24",
        "-r", "30",
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        outfile
    ]
    return ffmpeg_command

videos_dir="videos/"
if not os.path.exists(videos_dir):
    os.makedirs(videos_dir)

# Some probability of turning right by 0.1 radians
def update_custom(instance):
    prob = 0.03
    if random.random() < prob:
        instance.rot += 0.1

def generate_video(outfile, num_bees, fwd_amount, turn_amount, is_fullrand, screen_dim=(512, 512), video_dir=videos_dir):
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
    
    output_file = f"{os.path.join(video_dir, outfile)}.h264"
    ffmpeg_process = subprocess.Popen(prepare_ffmpeg_cmd(output_file), stdin=subprocess.PIPE)
    print(ffmpeg_process)
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
        frame = pygame.surfarray.pixels3d(screen)
        frame_rgb24 = np.asarray(frame, dtype=np.uint8)
        ffmpeg_process.stdin.write(frame_rgb24.tobytes())
        frame_number += 1
    
    pygame.quit()
    return output_file

for f in os.listdir(videos_dir):
    os.remove(os.path.join(videos_dir, f))

with open("dataset.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    field = ["file", "class", "begin frame", "end frame"]
    writer.writerow(field)
    num_videos = 150
    for video_number in range(num_videos):
        title = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        if random.random() < 0.5:
            file = generate_video(title, 1, 2, 0.15, True)
            nn_class=1
        else:
            file = generate_video(title, 1, 2, 0.15, False)
            nn_class=2
        writer.writerow([os.path.abspath(file), nn_class, 50, 1000])
