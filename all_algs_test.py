import random

from next_fit import next_fit
from first_fit import first_fit, first_fit_decreasing
from best_fit import best_fit, best_fit_decreasing

# Set a seed for reproducibility
random.seed(42)

# Generate the same sequence of 10 random floats between 0.0 and 0.35
nums = [round(random.uniform(0.0, 0.35), 4) for _ in range(50)]

print(f"\nInput items: {nums}\n")

# Define algorithm list
algorithms = {
    'next_fit': next_fit,
    'first_fit': first_fit,
    'first_fit_decreasing': first_fit_decreasing,
    'best_fit': best_fit,
    'best_fit_decreasing': best_fit_decreasing,
}

# Run each algorithm
for name, algo in algorithms.items():
    items = nums.copy()
    assignment = [0] * len(items)
    free_space = []

    algo(items, assignment, free_space)

    waste = len(free_space) - sum(nums)

    print(f"{name:<25} → Bins used: {len(free_space):2d}, Waste: {waste:.4f}, Free space: {free_space}")
