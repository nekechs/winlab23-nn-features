import beesim
import tarfile
import subprocess

beesim.make_test_frames(1, (512, 512), 140, "dataset_1")
beesim.make_test_frames(2, (512, 512), 60, "dataset_1")
subprocess.run(["tar", "cvf", "dataset_1.tar", "dataset_1" ])

beesim.make_test_frames(1, (512, 512), 140, "dataset_2")
beesim.make_test_frames(2, (512, 512), 60, "dataset_2")
subprocess.run(["tar", "cvf", "dataset_2.tar", "dataset_2"])
