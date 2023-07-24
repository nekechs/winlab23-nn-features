import argparse
import numpy as np
import pathlib
import os
import subprocess
from make_dataset import DatasetGenerator, Simulator

# This is the directory that we are in
currentDir = pathlib.Path(__file__).parent.resolve()

#python version to run the training program 
python3PathTrain = '/koko/system/anaconda/envs/python38/bin'

# command to run the evaluation and training program 
trainCommand    = 'srun -G 1 python3 $TRAINPROGRAM --not_deterministic --epochs 10 --modeltype $MODEL --evaluate' # <eval-set> <a-set> <b-set> ... 

modelName = 'alexnet'

parser = argparse.ArgumentParser(
    description="Generate a series of datasets for feature analysis on bees"
)
parser.add_argument(
    '--programdir',
    type=str,
    required=False,
    default=currentDir,
    help='The place where the executables for VidActRecTrain.py and such are stored'
)
parser.add_argument(
    '--datapoints',
    type=int,
    required=False,
    default=10,
    help='The number of datapoints that you would like to use'
)
parser.add_argument(
    '--lowbias',
    type=float,
    required=True,
    default=0.0,
    help='The minimum bias value that you would like to use'
)
parser.add_argument(
    '--highbias',
    type=float,
    required=True,
    default=1.0,
    help='The maximum bias value that you would like to use'
)
parser.add_argument(
    '--width',
    type=int,
    required=True,
    default=256,
    help='The width of the input'
)
parser.add_argument(
    '--height',
    type=int,
    required=True,
    default=256,
    help='The height of the input'
)
parser.add_argument(
    '--samples',
    type=int,
    required=True,
    help='Number of total samples PER CLASS'
)
parser.add_argument(
    '--ttsplit',
    type=float,
    required=False,
    default=0.8,
    help='The test/train split that is required (percent that is reserved for training data)'
)
args = parser.parse_args()

globalProgramDirectory = pathlib.Path(args.programdir).resolve()
trainProgram = os.path.join(globalProgramDirectory, 'VidActRecTrain.py')

if args.ttsplit >= 1.0 or args.ttsplit <= 0:
    raise(Exception('Enter a test/train split that is between 0.0 and 1.0, please.'))

# Samples per class
total_spc = args.samples
train_spc = int(total_spc * args.ttsplit)
test_spc = total_spc - train_spc

maykr = DatasetGenerator((256, 256), Simulator, 4)
# Objective is to generate 2 tar files for one datapoint, one train.sh file, and one csv entry for that run
bias_list = np.linspace(args.lowbias, args.highbias, args.datapoints)
for i, bias_amt in enumerate(bias_list):
    print(f"Started generating dataset {i}")
    title = f"dataset_{i}"
    maykr.gendata_dir(bias_amt=bias_amt, samples_per_class=train_spc, dirname=f"{title}_train")
    maykr.gendata_dir(bias_amt=bias_amt, samples_per_class=test_spc, dirname=f"{title}_test")
    train_job_filename = f"train_{i}.sh"

    with open(train_job_filename,'w') as trainFile:
        trainFile.write("#!/usr/bin/bash \n")
        #trainFile.write("#SBATCH --gpus-per-node=1 \n")
        trainFile.write("# command to run \n \n")
        trainFile.write(f"cd {currentDir} \n")
        trainFile.write(f"export PATH={python3PathTrain}:$PATH \n")
        trainFile.write("echo start-is: `date` \n \n") # add start timestamp 
        traincommand_local = f"{trainCommand.replace('$TRAINPROGRAM',trainProgram)} {title}_test.tar {title}_train.tar"
        traincommand_local = traincommand_local.replace('$MODEL', modelName)

        trainFile.write(traincommand_local +  "\n") # write the training command to the training command
        trainFile.write("echo end-is: `date` \n \n") # add end timestamp
    
    subprocess.run(['sbatch', '-G', '1', '-o', f"trainlog_{i}.log", train_job_filename])

# sbatch -G 1 -o dataset_trainlog_0.log train_1.sh 