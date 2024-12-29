import re

def calculate_set_indices(num_items, set_fractions):
    set_indices = {}
    cumulative_fraction = 0.0
    for set_name, fraction in set_fractions.items():
        set_start_index = int(cumulative_fraction * num_items)
        cumulative_fraction += fraction
        set_end_index = int(cumulative_fraction * num_items)
        set_indices[set_name] = (set_start_index, set_end_index)

    return set_indices


# 0550060501_028_027__SXA000001.jpg -> 0550060501_028_027__SXA
# Used for filtering subsequent images / those that have the same prefix but vary in the numeric part after the last underscore.
def extract_image_key(filename):
    filename_without_extension = filename.rsplit('.', 1)[0]
    # Match everything up to the last numeric part
    match = re.match(r"^(.*?_[A-Za-z]+)", filename_without_extension)
    if match:
        return match.group(1)  # Return the matched part before numeric suffix
    return filename  # Return original if no match