import csv
from enum import Enum, unique
import random, time

from pathlib import Path

import requirements

DATA_DIRECTORY = Path('data')
DATA_DIRECTORY.mkdir(exist_ok=True) #if directory already exists, the parameter prevents an error from being raised

@unique
class PermutationType(Enum):
    RANDOMLY_DISTRIBUTED = 'random'

BIN_PACKING_ALGORITHMS = {
    'next_fit' : requirements.next_fit,
    'first_fit' : requirements.first_fit,
    'first_fit_decreasing' : requirements.first_fit_decreasing,
    'best_fit' : requirements.best_fit,
    'best_fit_decreasing' : requirements.best_fit_decreasing
}

def get_data_path(algorithm_name: str, permutation: PermutationType) -> Path:
    directory = DATA_DIRECTORY/algorithm_name #creates a subdirectory for that sorting algorithm.
    directory.mkdir(parents=True, exist_ok=True) #ensures the subdirectory exists.

    return (directory / permutation.name).with_suffix(suffix='.csv')# creates a file path like:
#data/shell_sort3/RANDOM.csv


def save_data(algorithm_name: str, size: int, permutation:PermutationType, wasted_amount: int) -> None:
    file_path = get_data_path(algorithm_name,permutation)

    with open(file_path,mode='a', newline='') as file:#appends to end of a file
        writer = csv.writer(file)
        writer.writerow([size,wasted_amount])


def generate_random_list(size: int, permutation: PermutationType) -> list[float]:
    nums = [round(random.uniform(0.1001, 0.9999), 4) for _ in range(size)]

    match permutation:
        case PermutationType.RANDOMLY_DISTRIBUTED:
            random.shuffle(nums)

    return nums



def run_benchmark(size: int)->None:
    for permutation in PermutationType:
        nums = generate_random_list(size,permutation)
        zeroes = [0] * size #not being used
        waste = [] #not being used
        #these are used to satisfy the positional arguments in each algorithm because they need both assignment and free_space
        

        for algorithm_name, algorithm in BIN_PACKING_ALGORITHMS.items():
            #copy the list to ensure each algorithm works with the same input
            nums_copy = nums.copy()
            zeroes_copy = zeroes.copy()
            waste_copy = waste.copy()
            #start_time_ns = time.process_time_ns()

            algorithm(nums_copy,zeroes_copy,waste_copy)

            #end_time_ns = time.process_time_ns()
            #elapsed_time_ns = end_time_ns - start_time_ns
            waste_result = len(waste_copy) - sum(waste_copy)

            save_data(algorithm_name,size,permutation,waste_result)

def run_benchmarks(): #should do 10 runs of up to 2^16
    for round_num in range(734): #we want to run for 2000 runs, so lets make 200 jobs
        #change back to 10 to do 10 runs later
        print(f"\n=== Round {round_num + 1}/10 ===")

        for exp in range(1, 20):  # from 2^1 to 2^20
            size = 2 ** exp
            print(f"Running benchmark for size: {size}")
            start_time_ns = time.process_time_ns()

            run_benchmark(size)

            end_time_ns = time.process_time_ns()
            elapsed_time_ns = end_time_ns - start_time_ns
            print(f"Benchmark completed in {elapsed_time_ns / 1_000_000:.2f} ms")

if __name__ == "__main__":
    run_benchmarks()
    #run_benchmarks_alternating()