from pathlib import Path
import csv
from collections import defaultdict

def calc_average(perumutation_data):
    averages = {
        'ALMOST_SORTED' : {},
        'ALTERNATING' : {},
        'UNIFORMLY_DISTRIBUTED' : {}
    }


    for perm_type, sizes in perumutation_data.items():
        for size,times in sizes.items():
            averages[perm_type][size] = sum(times)//len(times)

    return averages

def load_all_data(directory: Path):
    data = {
        'ALMOST_SORTED' : defaultdict(list),
        'ALTERNATING' : defaultdict(list),
        'UNIFORMLY_DISTRIBUTED' : defaultdict(list)
    }

    for file in directory.glob("*.csv"): #gets all csv files in the given directory
        permutation_type = file.stem

        with open(file, mode='r') as f:
            reader = csv.reader(f)
            for row in reader:
                size, time_ns = map(int, row) #turns rows of two elements such as
                #3,3 into [3,3]

                data[permutation_type][size].append(time_ns)

    return calc_average(data)
    

def load_all_folders(base_directory: Path = Path("data")):
    all_data = {}

    for subfolder in base_directory.iterdir():# Iterate over all subfolders in the base directory
        if subfolder.is_dir():# Only process directories
            folder_data = load_all_data(subfolder)# Call the existing function for each subfolder
            all_data[subfolder.name] = folder_data# Store the data for this folder

    return all_data


def return_all_data():
    base_directory = Path.cwd() / "data"  # Set your base directory path
    all_data = load_all_folders(base_directory)  # Call the function to load all folder data
    return all_data


if __name__ == "__main__":
    base_directory = Path.cwd() / "data"  # Set your base directory path
    all_data = load_all_folders(base_directory)  # Call the function to load all folder data
    
    # Optionally, print the result to check the output
    print(all_data)
