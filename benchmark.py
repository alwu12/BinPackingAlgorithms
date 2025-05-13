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


def save_data(algorithm_name: str, size: int, permutation:PermutationType, elapsed_time_ns: int) -> None:
    file_path = get_data_path(algorithm_name,permutation)

    with open(file_path,mode='a') as file:#appends to end of a file
        writer = csv.writer(file)
        writer.writerow([size,elapsed_time_ns])


def generate_random_list(size: int, permutation: PermutationType) -> list[int]:
    nums = list(range(size))

    match permutation:
        case PermutationType.UNIFORMLY_DISTRIBUTED:
            random.shuffle(x=nums)
        #case PermutationType.ALTERNATING:
        #    nums = [i for i in range(1, size + 1, 2)] + [i for i in range(2, size + 1, 2)]
        #case PermutationType.ALMOST_SORTED:
            # Introduce a small number of random swaps to make the list almost sorted
        #    num_swaps = size // 10  # For example, 10% of the list size
        #    for _ in range(num_swaps):
        #        i, j = random.sample(range(size), 2)
        #        nums[i], nums[j] = nums[j], nums[i]

    return nums


def run_benchmark(size: int)->None:
    for permutation in PermutationType:
        nums = generate_random_list(size,permutation)

        for algorithm_name, algorithm in BIN_PACKING_ALGORITHMS.items():
            #copy the list to ensure each algorithm works with the same input
            nums_copy = nums.copy()

            start_time_ns = time.process_time_ns()

            algorithm(nums_copy)

            end_time_ns = time.process_time_ns()
            elapsed_time_ns = end_time_ns - start_time_ns

            save_data(algorithm_name,size,permutation,elapsed_time_ns)

def run_benchmarks(): #should do 10 runs of up to 2^16
    for round_num in range(1): #we want to run for 2000 runs, so lets make 200 jobs
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