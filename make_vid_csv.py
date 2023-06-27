import beesim
import csv
from datetime import datetime
import random
import os

with open('dataset.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    field = ["file", "class", "begin frame", "end frame"]
    writer.writerow(field)
    num_videos = 150
    for video_number in range(num_videos):
        title = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        if random.random() < 0.5:
            nn_class=1
        else:
            nn_class=2
        print(nn_class)
        beesim.make_test_frames(nn_class, (256, 256))
        file = beesim.assemble_video(title)
        writer.writerow([os.path.abspath(file), nn_class, 50, 1000])