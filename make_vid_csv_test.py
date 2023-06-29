import beesim
import csv
from datetime import datetime
import random
import os

with open('dataset.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    field = ["file", "class", "begin frame", "end frame"]
    writer.writerow(field)

    beesim.make_test_frames(1, (256, 256), 4005)
    title = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
    file = beesim.assemble_video(title)
    writer.writerow([os.path.abspath(file), 1, 0, 500])
    
    beesim.make_test_frames(2, (256, 256), 4005)
    title = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
    file = beesim.assemble_video(title)
    writer.writerow([os.path.abspath(file), 2, 0, 500])