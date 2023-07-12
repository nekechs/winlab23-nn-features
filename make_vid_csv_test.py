import beesim
import numpy as np
import pygame
from datetime import datetime
import subprocess
import os

def draw_rand_rectangle(screen: pygame.surface.Surface, color=(0, 0, 0)):
    arr = np.random.rand(2, 2)
    arr.sort(axis=1)
    (screen_width, screen_height) = screen.get_size()
    left = arr[0][0] * screen_width
    top = arr[1][0] * screen_height
    width = (arr[0][1] - arr[0][0]) * screen_width
    height = (arr[1][1] - arr[1][0]) * screen_height

    pygame.draw.rect(screen, color, pygame.Rect(
        left,
        top,
        width,
        height
    ))

pacsurf = pygame.Surface((32, 32), pygame.SRCALPHA)
pygame.draw.circle(pacsurf, (0, 0, 0), (16, 16), 16, False, True, True, True)

def rand_dir(prob: 0.5):
    if np.random.rand(1,) < prob:
        return -1
    else:
        return 1

def draw_pacman_angle(screen: pygame.surface.Surface, x: int, y: int, angle, color=(0, 0, 0)):
    rot_surf = pygame.transform.rotate(pacsurf, angle)
    rot_rect = rot_surf.get_rect(center=(x, y))
    screen.blit(rot_surf, rot_rect)

def make_multiple_frames(classnum, screen_dim, frames_per_sample=1, num_samples=1024, frames_dir="frames", video_dir="videos"):
    (x_dim, y_dim) = screen_dim
    pygame.init()
    screen = pygame.display.set_mode([x_dim, y_dim])

    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)
    
    fake_filename = datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S_%f_h264')
    fake_filepath = datetime.utcnow().strftime('FAKEPATH/%Y-%m-%d %H:%M:%S.%f.h264')

    sample_num = 0
    while sample_num < num_samples:
        sample_name = f"{fake_filename}_{sample_num + 1}"

        # Save the class files and metadata file for this example
        class_filename = os.path.join(frames_dir, f"{sample_name}.cls")
        md_filename = os.path.join(frames_dir, f"{sample_name}.metadata.txt")
        with open(class_filename, 'w') as file:
            file.write(f"{classnum}")
        with open(md_filename, 'w') as file:
            file.write(f"{fake_filepath},{sample_num + 1},{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")

        # implementation specific
        start_coords = np.random.rand(2,)
        # (x, y) = (start_coords[0] * x_dim, start_coords[1] * y_dim)
        (x, y) = (x_dim // 2, y_dim // 2)
        angle = int(np.random.rand(1,) * 360)

        frame_num = 0
        while frame_num < frames_per_sample:
            # Here is where the actual pygame code starts
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            screen.fill((255, 255, 255))
            if classnum == 1:
                draw_pacman_angle(screen, x, y, angle)
                angle += rand_dir(0.5) * 15
            if classnum == 2:
                draw_pacman_angle(screen, x, y, angle)
                angle += rand_dir(0.5) * 15

            pygame.display.flip()
            frame_filename = os.path.join(frames_dir, f"{sample_name}.{frame_num}.png")

            pygame.image.save(screen, frame_filename)
            frame_num += 1
        sample_num += 1


def make_test_frames(classnum, screen_dim, frames_per_sample=1, num_frames=1024, frames_dir="frames", video_dir="videos"):
    (x_dim, y_dim) = screen_dim
    pygame.init()
    screen = pygame.display.set_mode([x_dim, y_dim])
    
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)

    fake_filename = datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S_%f_h264')
    fake_filepath = datetime.utcnow().strftime('FAKEPATH/%Y-%m-%d %H:%M:%S.%f.h264')
    
    frame_number = 1
    frame_number_start = frame_number

    while frame_number < num_frames:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill((255, 255, 255))
        if classnum == 1:
            # draw_rand_rectangle(screen, (0, 0, 0))
            draw_pacman_angle(screen, 200, 200, 0)
        if classnum == 2:
            draw_pacman_angle(screen, 200, 200, 180)
            # draw_rand_rectangle(screen, (0, 0, 0))
            # draw_rand_rectangle(screen, (0, 0, 0))
            # screen.fill((0, 0, 0))

        # if random.random() < 0.5:
        #     screen.fill((255, 255, 255))
        # else:
        #     screen.fill((0, 0, 0))

        pygame.display.flip()
        frame_filename = os.path.join(frames_dir, f"{fake_filename}_{frame_number}.0.png")
        class_filename = os.path.join(frames_dir, f"{fake_filename}_{frame_number}.cls")
        md_filename = os.path.join(frames_dir, f"{fake_filename}_{frame_number}.metadata.txt")

        pygame.image.save(screen, frame_filename)
        with open(class_filename, 'w') as file:
            file.write(f"{classnum}")
        with open(md_filename, 'w') as file:
            file.write(f"{fake_filepath},{frame_number},{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
        frame_number += 1

# make_test_frames(1, (512, 512), num_frames=1000, frames_dir="dataset_1")
# make_test_frames(2, (512, 512), num_frames=1000, frames_dir="dataset_1")
# subprocess.run(["tar", "cvf", "dataset_1.tar", "dataset_1" ])
# 
# make_test_frames(1, (512, 512), num_frames=100, frames_dir="dataset_2")
# make_test_frames(2, (512, 512), num_frames=100, frames_dir="dataset_2")
# subprocess.run(["tar", "cvf", "dataset_2.tar", "dataset_2"])


make_multiple_frames(1, (224, 224), frames_per_sample=4, num_samples=1000, frames_dir="dataset_1")
make_multiple_frames(2, (224, 224), frames_per_sample=4, num_samples=1000, frames_dir="dataset_1")
subprocess.run(["tar", "cvf", "dataset_1.tar", "dataset_1" ])

make_multiple_frames(1, (224, 224), frames_per_sample=4, num_samples=100, frames_dir="dataset_2")
make_multiple_frames(2, (224, 224), frames_per_sample=4, num_samples=100, frames_dir="dataset_2")
subprocess.run(["tar", "cvf", "dataset_2.tar", "dataset_2"])