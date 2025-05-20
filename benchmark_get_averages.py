from pathlib import Path
import csv
from collections import defaultdict

def calc_average(bin_packing_data):
    '''
    BIN_PACKING_ALGORITHMS = {
        'next_fit' : {},
        'first_fit' : {},
        'first_fit_decreasing' : {},
        'best_fit' : {},
        'best_fit_decreasing' : {}
    }'''

    averages = {}


    for size,waste in bin_packing_data.items():
        averages[size] = sum(waste)/len(waste)

    return averages

def load_all_data(directory: Path):
    data = defaultdict(list)

    for file in directory.glob("*.csv"): #gets all csv files in the given directory
        with open(file, mode='r') as f:
            reader = csv.reader(f)
            for row in reader:
                size, time_ns = map(float, row) #turns rows of two elements such as
                #3,3 into [3,3]

                data[int(size)].append(time_ns)

    return calc_average(data)
    

def load_all_folders(base_directory: Path = Path("data")):
    all_data = {}#makes a dictionary with all the file names as the keys
    #in my case it makes
    '''
    all_data = {
        'next_fit' : {},
        'first_fit' : {},
        'first_fit_decreasing' : {},
        'best_fit' : {},
        'best_fit_decreasing' : {}
    }'''


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
    #print(all_data)
