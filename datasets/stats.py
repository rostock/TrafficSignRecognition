"""
This script aggregates statistics for any of the YOLOv8 segmentation datasets.

Should be called with one parameter: the dataset name, e.g. tsr_example.

> python3 datasets/stats.py tsr_example

Output looks like this:

Statistics for train set:
 - 205_vorfahrt_gewaehren: 19
 - 206_halt_vorfahrt_gewaehren: 3
 - 123_arbeitsstelle: 3
 - 250_verbot_alle: 1
 - 283_absolutes_halteverbot: 51
 - 286_eingeschraenktes_halteverbot: 13
 - 283_10_absolutes_halteverbot_anfang_rechts: 8
 - ...

Statistics for val set:
 - 205_vorfahrt_gewaehren: 3
 - ...

Statistics for test set:
 - 205_vorfahrt_gewaehren: 6
 - 250_verbot_alle: 2
 - ...

"""
import yaml
import os
import argparse
from collections import defaultdict

def count_classes(annotations_file_path):
    class_counts = defaultdict(int)
    with open(annotations_file_path, 'r') as file:
        for label_line in file:
            class_id = int(label_line.split()[0])
            class_counts[class_id] += 1
    return class_counts

def aggregate_statistics(dataset_path_absolute):
    sets = ['train', 'val', 'test']
    statistics = {}

    for set_name in sets:
        statistics[set_name] = {}

        setPath = os.path.join(dataset_path_absolute, "labels", set_name)
        for file in os.listdir(setPath):
            if file.endswith(".txt"):
                file_path = os.path.join(setPath, file)
                stats = count_classes(file_path)
                # merge stats with existing statistics
                for class_id, count in stats.items():
                    statistics[set_name][class_id] = statistics[set_name].get(class_id, 0) + count

    return statistics

def getNamesForIds(dataset_path_absolute):
    names = {}
    with open(os.path.join(dataset_path_absolute, "data.yaml"), 'r') as file:
        data = yaml.safe_load(file)
        for id, name in data['names'].items():
            names[int(id)] = name
    return names

def print_statistics(statistics, dataset_path_absolute):
    names = getNamesForIds(dataset_path_absolute)
    for set_name, class_counts in statistics.items():
        print(f"Statistics for {set_name} set:")
        for class_id, count in sorted(class_counts.items()):
            print(f" - {names[class_id]}: {count}")
        print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Aggregate statistics for YOLOv8 segmentation dataset')
    parser.add_argument('dataset', help='Dataset name, e.g. tsr_example')
    args = parser.parse_args()

    dataset_path_absolute = os.path.abspath(os.path.join(os.path.dirname(__file__), args.dataset))

    if not os.path.exists(dataset_path_absolute):
        print(f"Dataset folder {dataset_path_absolute} does not exist.")
        exit(1)

    statistics = aggregate_statistics(dataset_path_absolute)
    print_statistics(statistics, dataset_path_absolute)