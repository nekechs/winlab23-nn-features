import subprocess
import numpy as np
import pygame
from abc import ABC, abstractmethod
from datetime import datetime
import tarfile
import os

# This is the name of the temporary dump directory for each dataset
dumpname = '__tarcontent__'

pac_radius = 16
pacsurf = pygame.Surface((pac_radius * 2, pac_radius * 2), pygame.SRCALPHA)
pygame.draw.circle(pacsurf, (0, 0, 0), (pac_radius, pac_radius), pac_radius, False, True, True, True)

class Simulator(ABC):
    @abstractmethod
    def __init__(self, screen: pygame.surface.Surface, bias_amt):
        pass

    @abstractmethod
    def draw(self):
        pass

    # Randomly resets the state of the simulation
    @abstractmethod
    def reset(self):
        pass

    # This function advances the timestep by 1
    # Classnum 1 - random; classnum 2 - non random
    @abstractmethod
    def update(self, classnum):
        pass

class LeftRightSimulator(Simulator):
    def __init__(self, screen: pygame.surface.Surface, bias_amt):
        (self.x_dim, self.y_dim) = screen.get_size()
        self.pos = (self.x_dim // 2, self.y_dim // 2)
        self.bias_amt = bias_amt

        self.angle = 0
        self.reset()
    
        # Pygame specific details
        self.radius = 128
        self.circlesurf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.circlesurf, (0, 0, 0), (self.radius, self.radius), self.radius, False, True, True, True)
        # pygame.init()
        self.screen = screen

        # Based on the current angle, draw the pacman onto the screen
    def draw_pacman_angle(self):
        rot_surf = pygame.transform.rotate(self.circlesurf, self.angle)
        rot_rect = rot_surf.get_rect(center=self.pos)
        self.screen.blit(rot_surf, rot_rect)

    def draw(self):
        self.screen.fill((255, 255, 255))
        # draw_pacman_angle(self.screen, self.pos[0], self.pos[1], self.angle)
        self.draw_pacman_angle()

    # Randomly resets the state of the simulation
    def reset(self):
        self.angle = np.random.rand(1,) * 360

    def update(self, classnum):
        delta_angle = np.random.uniform(1, 5)
        delta_angle = -delta_angle if classnum == 1 else delta_angle
        self.angle += delta_angle

class PacmanSimulator(Simulator):
    def __init__(self, screen: pygame.surface.Surface, bias_amt):
        # Parameters of the simulation that stay the same
        (self.x_dim, self.y_dim) = screen.get_size()
        self.pos = (self.x_dim // 2, self.y_dim // 2)
        self.bias_amt = bias_amt

        # Parameters of the simulation that get randomized
        self.angle = 0
        self.reset()
 
        # Pygame specific details
        self.radius = 128
        self.circlesurf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.circlesurf, (0, 0, 0), (self.radius, self.radius), self.radius, False, True, True, True)
        # pygame.init()
        self.screen = screen

    # Based on the current angle, draw the pacman onto the screen
    def draw_pacman_angle(self):
        rot_surf = pygame.transform.rotate(self.circlesurf, self.angle)
        rot_rect = rot_surf.get_rect(center=self.pos)
        self.screen.blit(rot_surf, rot_rect)

    def draw(self):
        self.screen.fill((255, 255, 255))
        # draw_pacman_angle(self.screen, self.pos[0], self.pos[1], self.angle)
        self.draw_pacman_angle()

    # Randomly resets the state of the simulation
    def reset(self):
        self.angle = np.random.rand(1,) * 360
    
    # This function advances the timestep by 1
    # Classnum 1 - random; classnum 2 - non random
    def update(self, classnum):
        bias = 0 if classnum == 1 else self.bias_amt
        delta_angle = np.random.uniform(-10, 10)
        if np.random.rand(1,) < 0.5:
            # delta_angle = -(np.random.rand(1,) * 4 + 1)
            pass
        else:
            # delta_angle = (np.random.rand(1,) * 4 + 1) + bias
            delta_angle += bias
        self.angle += delta_angle

class BWSimulator(Simulator):
    def __init__(self, screen: pygame.surface.Surface, bias_amt):
        # Params of simulation that stay the same
        self.x_dim, self.y_dim = screen.get_size()
        self.bias_amt = bias_amt

        # Parameters of the simulation subject to change
        self.brightness = 0.0
        
        # Pygame specific details
        self.screen = screen

    def draw(self):
        self.screen.fill((self.brightness * 255, self.brightness * 255, self.brightness * 255))

    def reset(self):
        self.brightness = 0.0

    def update(self, classnum):
        self.brightness = 0.0 if classnum == 1 else 1.0

# What is the intention of the dataset generator?
# Simple: Generate a dataset through a predefined simulator
class DatasetGenerator:
    def __init__(self, screen_dim, Cls, frames_per_sample=1):
        self.screen_dim = screen_dim
        self.frames_per_sample = frames_per_sample

        if not issubclass(Cls, Simulator):
            fstr = f"{Cls.__name__} and {Simulator.__name__}"
            print(fstr)
            raise TypeError(f"{Cls.__name__} is not an instance of {Simulator.__name__}")
        self.simcls = Cls
    
    # Produce one dataset of the simulation (essentially create directory containing elems of tarfiles)
    def gendata_dir(self, bias_amt, samples_per_class, dirname):
        (x_dim, y_dim) = self.screen_dim
        pygame.init()
        screen = pygame.display.set_mode([x_dim, y_dim])
        simulation = self.simcls(screen, bias_amt)
        
        if os.path.exists(dirname):
            subprocess.run(["rm", "-rf", dirname])
        os.makedirs(dirname)

        # Generate frames and put frames inside of directory.
        tar = tarfile.open(f"{dirname}.tar", 'w')
        for classnum in range(1, 3):
            fake_filename = datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S_%f_h264')
            fake_filepath = datetime.utcnow().strftime('FAKEPATH/%Y-%m-%d %H:%M:%S.%f.h264')
            for sample_num in range(samples_per_class):
                # Logistics
                sample_name = f"{fake_filename}_{sample_num + 1}"
                class_filename = os.path.join(dirname, f"{sample_name}.cls")
                md_filename = os.path.join(dirname, f"{sample_name}.metadata.txt")

                # We must add these to the tarfile after the pngs are added
                with open(class_filename, 'w') as file:
                    file.write(f"{classnum}")
                with open(md_filename, 'w') as file:
                    file.write(f"{fake_filepath},{sample_num + 1},{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
                
                simulation.reset()
                for framecount in range(self.frames_per_sample):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.exit()
                            exit()
                    
                    simulation.update(classnum)
                    simulation.draw()

                    pygame.display.flip()
                    frame_filename = os.path.join(dirname, f"{sample_name}.{framecount}.png")
                    pygame.image.save(screen, frame_filename)
                    tar.add(frame_filename)
                    # os.remove(frame_filename)
                
                tar.add(class_filename)
                tar.add(md_filename)
                # os.remove(class_filename)
                # os.remove(md_filename)

        tar.close()

# gen = DatasetGenerator((256, 256), Simulator, 1)
# gen.gendata_dir(10.0, 2, 'dataset_train')
# gen.gendata_dir(10.0, 2, 'dataset_test')