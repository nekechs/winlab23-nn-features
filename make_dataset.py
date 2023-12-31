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