#!/bin/bash

# Check if the subfolder name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <subfolder>"
  exit 1
fi

parent_path=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$parent_path" || exit

SUBFOLDER=$1

# Define the files to be processed
FILES=("train.txt" "test.txt" "val.txt")

# Loop through each file and perform the replacement
for FILE in "${FILES[@]}"; do
  FILE_PATH="$SUBFOLDER/$FILE"
  if [ -f "$FILE_PATH" ]; then
    sed -i 's|data/|datasets/'"$SUBFOLDER"'/|g' "$FILE_PATH"
  else
    echo "File $FILE_PATH does not exist."
    exit 1
  fi
done

# Update the data.yaml file
DATA_YAML_PATH="$SUBFOLDER/data.yaml"
if [ -f "$DATA_YAML_PATH" ]; then
  sed -i 's|path: .|path: /usr/src/datasets/'"$SUBFOLDER"'/|g' "$DATA_YAML_PATH"
  sed -i 's|train: train.txt|train: images/train|g' "$DATA_YAML_PATH"
  sed -i 's|test: test.txt|test: images/test|g' "$DATA_YAML_PATH"
  sed -i 's|val: val.txt|val: images/val|g' "$DATA_YAML_PATH"
else
  echo "File $DATA_YAML_PATH does not exist."
  exit 1
fi

echo "Paths have been fixed for dataset $SUBFOLDER."

