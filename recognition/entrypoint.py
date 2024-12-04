import argparse
from src import train, inference

parser = argparse.ArgumentParser(prog='recognition/run.sh', description='Traffic Sign Recognition')
parser.add_argument('method', nargs=1, help='train or inference')
parser.add_argument('dataset', nargs=1, help='dataset name, e.g. tsr_example')
args = parser.parse_args()

if args.method[0] == 'train':
    print("Training model on dataset " + args.dataset[0])
    train(args.dataset[0])
elif args.method[0] == 'inference':
    print("Performing inference on dataset " + args.dataset[0])
    inference(args.dataset[0])
else:
    print("Invalid method")

print("Using method " + args.method[0] + " dataset " + args.dataset[0])

print(args)
