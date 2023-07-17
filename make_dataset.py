import subprocess
import numpy as np
import pygame
from datetime import datetime
import tarfile
import os

# This is the name of the temporary dump directory for each dataset
dumpname = '__tarcontent__'

pac_radius = 16
pacsurf = pygame.Surface((pac_radius * 2, pac_radius * 2), pygame.SRCALPHA)
pygame.draw.circle(pacsurf, (0, 0, 0), (pac_radius, pac_radius), pac_radius, False, True, True, True)

def draw_pacman_angle(screen: pygame.surface.Surface, x: int, y: int, angle, color=(0, 0, 0)):
    rot_surf = pygame.transform.rotate(pacsurf, angle)
    rot_rect = rot_surf.get_rect(center=(x, y))
    screen.blit(rot_surf, rot_rect)

def generate_dataset(screen_dim, strength, frames_per_sample=1, samples_per_class=1024, title='frames'):
    (x_dim, y_dim) = screen_dim
    pygame.init()
    screen = pygame.display.set_mode([x_dim, y_dim])

    subprocess.run(["rm", "-rf", "__tarcontent__"])
    if not os.path.exists('__tarcontent__'):
        os.makedirs('__tarcontent__')

    # First, we need to generate the frames and put all files in __tarcontent__
    for classnum in range(1, 3):
        print(classnum)
        fake_filename = datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S_%f_h264')
        fake_filepath = datetime.utcnow().strftime('FAKEPATH/%Y-%m-%d %H:%M:%S.%f.h264')
        for sample_num in range(samples_per_class):
            # Things relevant to this trial
            sample_name = f"{fake_filename}_{sample_num + 1}"
            class_filename = os.path.join('__tarcontent__', f"{sample_name}.cls")
            md_filename = os.path.join('__tarcontent__', f"{sample_name}.metadata.txt")
            with open(class_filename, 'w') as file:
                file.write(f"{classnum}")
            with open(md_filename, 'w') as file:
                file.write(f"{fake_filepath},{sample_num + 1},{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")

            # This is specific to implementation:
            start_coords = np.random.rand(2,)
            (x, y) = (x_dim // 2, y_dim // 2)
            angle = int(np.random.rand(1,) * 360)

            for frame in range(frames_per_sample):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                
                screen.fill((255, 255, 255))
                randnum = np.random.rand(1,)
                if classnum == 1:
                    thresh = 0.5
                else:
                    thresh = strength
                
                delta_angle = -15 if randnum < thresh else 15
                draw_pacman_angle(screen, x, y, angle)
                angle += delta_angle

                pygame.display.flip()
                frame_filename = os.path.join('__tarcontent__', f"{sample_name}.{frame}.png")
                pygame.image.save(screen, frame_filename)

    # Now we need to put it all in a tarfile
    tar = tarfile.open(f"{title}.tar", 'w')
    for filename in os.listdir('__tarcontent__'):
        filepath = os.path.join('__tarcontent__', filename)
        print(filepath)
        tar.add(filepath)
    tar.close()

generate_dataset((224, 224), strength=1.0, frames_per_sample=4, samples_per_class=1000, title='dataset_1_train')
generate_dataset((224, 224), strength=1.0, frames_per_sample=4, samples_per_class=100, title='dataset_1_train')