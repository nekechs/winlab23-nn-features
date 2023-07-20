import argparse
import numpy as np
from make_dataset import DatasetGenerator, Simulator

parser = argparse.ArgumentParser(
    description="Generate a series of datasets for feature analysis on bees"
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
    print(f"Started training dataset {i}")
    title = f"dataset_{i}"
    maykr.gendata_dir(bias_amt=bias_amt, samples_per_class=train_spc, dirname=f"{title}_train")
    maykr.gendata_dir(bias_amt=bias_amt, samples_per_class=test_spc, dirname=f"{title}_test")

