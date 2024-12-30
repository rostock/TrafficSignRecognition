from preprocessing.utils import calculate_set_indices, extract_image_key

"""
    Filter & Restructure source images:
        1) filter out subsequent images of the same street (too similar images)
        2) randomize order of images
        3) split into train, validation, test sets
        4) copy images to new flatter directory structure

    Photos are supposed to be inside folders like this: 
        Photos/0770079603/050_052_/SXA000053.jpg
    
    The photos will be copied to a new flat directory structure like this:
        Photos_filteres/train/0770079603_050_052_SXA000053.jpg

"""

###################################
#           Configuration         #
###################################
image_path = r"C:\Users\alexa\Downloads\Fotos"
output_path = r"C:\Users\alexa\Downloads\Fotos_filtered"
set_fractions = {"train": 0.7, "test": 0.2, "val": 0.1}

###################################
#      Validate Configuration     #
###################################

import os
import shutil
import random
from tqdm import tqdm

# Ensure sets add up to 1.0
assert sum(set_fractions.values()) == 1, "set fractions must sum to 1.0"

###################################
#  Filter & Create new Filenames  #
###################################
filecount = 0
file_info_for_image_key = {}
for root, _, files in os.walk(image_path):
    for file in sorted(files):  # Sort files to ensure order
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            filecount += 1
            old_file_path = os.path.join(root, file)

            # Add subdirectory path into new filename
            new_file_name = os.path.relpath(old_file_path, image_path).replace(os.sep, '_')

            image_key = extract_image_key(new_file_name)
            # print(logical_prefix, file_path)
            if image_key not in file_info_for_image_key:
                file_info_for_image_key[image_key] = [old_file_path, new_file_name]

print(filecount, len(file_info_for_image_key))


###################################
#   Randomize & Split into Sets   #
###################################
all_image_keys = list(file_info_for_image_key.keys())
random.shuffle(all_image_keys)
num_image_keys = len(all_image_keys)

image_keys_by_set_name = {
    set_name: all_image_keys[set_start_index:set_end_index]
    for set_name, (set_start_index, set_end_index) in calculate_set_indices(num_image_keys, set_fractions).items()
}

print(f"Processing complete. {filecount} images were filtered to {num_image_keys} images and set into sets:",
      [[set_name, len(image_keys_by_set_name[set_name])] for set_name in image_keys_by_set_name.keys()])

###################################
#  Copy images to the new folder  #
###################################
# Copy images to their respective directories
for set_name, image_keys in image_keys_by_set_name.items():
    os.makedirs(os.path.join(output_path, set_name))
    for image_key in tqdm(image_keys, desc=f"Copying {set_name} images", unit="image"):
        old_file_path, new_file_name = file_info_for_image_key[image_key]
        new_file_path = os.path.join(output_path, set_name, new_file_name)
        # print("Copying", old_file_path, "to", new_file_path)
        shutil.copy(old_file_path, new_file_path)
