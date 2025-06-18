import os
import argparse
from src import train, inference

parser = argparse.ArgumentParser(prog='recognition/run.sh', description='Traffic Sign Recognition')
parser.add_argument('method', nargs=1, help='train or inference')
parser.add_argument('dataset', nargs=1, help='dataset name, e.g. tsr_example')
parser.add_argument('--resume', action='store_true', help='resume training from last checkpoint?')

args = parser.parse_args()

dataset = args.dataset[0]

dataset_path = os.path.join("../datasets/", dataset)
dataset_path_absolute = os.path.abspath(dataset_path)

if not os.path.exists(dataset_path):
    print(f"Dataset folder {dataset_path} does not exist.")
    exit(1)

if args.method[0] == 'train':
    print("Training model on dataset " + dataset)
    train(dataset_path_absolute, args.resume)
elif args.method[0] == 'inference':
    print("Performing inference on dataset " + dataset)
    inference(dataset_path_absolute)
else:
    print("Invalid method")

print("Using method " + args.method[0] + " dataset " + dataset)

print(args)
