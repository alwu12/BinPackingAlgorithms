import random
from zipzipbf import ZipZipTreeBF
from best_fit import best_fit  # Adjust import if needed
from decimal import Decimal


def check_tree_for_cycles(root):
    visited = set()

    def dfs(node):
        if node is None:
            return False
        if id(node) in visited:
            print(f"Cycle detected at node with key: {node.key}")
            return True
        visited.add(id(node))
        return dfs(node.left) or dfs(node.right)

    return dfs(root)

def run_best_fit_with_1500000_items():
    items = [random.uniform(0.01, 0.99) for _ in range(150000)]

    assignment = [0] * len(items)
    free_space = []

    # Call best_fit algorithm
    tree = best_fit(items, assignment, free_space)

    print(f"Total bins used: {len(set(assignment))}")

    # Check for cycles
    if check_tree_for_cycles(tree.root):
        print("❌ Cycle detected in the tree.")
    else:
        print("✅ No cycles detected in the tree.")


def test_random_insert_remove(n=10, seed=42):
    random.seed(seed)

    tree = ZipZipTreeBF(capacity=1.0)
    inserted_keys = []

    for i in range(n):
        size = Decimal(str(random.randint(0, n // 4))) / Decimal(str(n))  # size between 0 and 0.25
        key = (Decimal('1.0') - size,i)
        tree.insert(key, 1)
        inserted_keys.append(key)
        print(f'just inserted {key}\n')
        tree.print_tree()
        print(f'\n')

    print(f"Inserted keys: {inserted_keys}")
    print(f"Inserted {len(inserted_keys)} keys.")
    
    print(f"Tree size after insertions: {tree.size}")

    print(f"tree's current root: {tree.root}")
    tree.print_tree()
    random.shuffle(inserted_keys)

    for key in inserted_keys:
        tree.remove(key)

    print(f"Tree size after deletions: {tree.size}")

def test_best_fit_10_items(seed=42):
    random.seed(seed)
    items = [round(random.uniform(0.01, 0.99), 2) for _ in range(10)]
    print(f"Items: {items}")

    assignment = [0] * len(items)
    free_space = []

    tree = best_fit(items, assignment, free_space)

    print(f"\nAssignments: {assignment}")
    print(f"Free space per bin (actual waste): {free_space}")
    print(f"Total bins used: {len(set(assignment))}")

    # Check for cycles in the tree
    if check_tree_for_cycles(tree.root):
        print("❌ Cycle detected in the tree.")
    else:
        print("✅ No cycles detected in the tree.")

    # Compute expected waste per bin
    expected_waste = []
    num_bins = len(set(assignment))
    for bin_id in range(num_bins):
        bin_sum = sum(items[i] for i in range(len(items)) if assignment[i] == bin_id)
        waste = round(1.0 - bin_sum, 6)
        expected_waste.append(waste)

    print(f"Expected waste: {expected_waste}")

    # Compare actual and expected waste
    print("\nComparing actual vs expected waste...")
    for i, (actual, expected) in enumerate(zip(free_space, expected_waste)):
        if abs(actual - expected) > 1e-6:
            print(f"❌ Bin {i}: actual={actual:.6f}, expected={expected:.6f}")
        else:
            print(f"✅ Bin {i}: matches (waste = {actual:.6f})")
    
def test_best_fit_20_items(seed=42):
    random.seed(seed)
    items = [round(random.uniform(0.01, 0.99), 2) for _ in range(20)]
    print(f"Items: {items}")

    assignment = [0] * len(items)
    free_space = []

    tree = best_fit(items, assignment, free_space)

    print(f"\nAssignments: {assignment}")
    print(f"Free space per bin (actual waste): {free_space}")
    print(f"Total bins used: {len(set(assignment))}")

    # Check for cycles in the tree
    if check_tree_for_cycles(tree.root):
        print("❌ Cycle detected in the tree.")
    else:
        print("✅ No cycles detected in the tree.")

    # Compute expected waste per bin
    expected_waste = []
    num_bins = len(set(assignment))
    for bin_id in range(num_bins):
        bin_sum = sum(items[i] for i in range(len(items)) if assignment[i] == bin_id)
        waste = round(1.0 - bin_sum, 6)
        expected_waste.append(waste)

    print(f"Expected waste: {expected_waste}")

    # Compare actual and expected waste
    print("\nComparing actual vs expected waste...")
    for i, (actual, expected) in enumerate(zip(free_space, expected_waste)):
        if abs(actual - expected) > 1e-6:
            print(f"❌ Bin {i}: actual={actual:.6f}, expected={expected:.6f}")
        else:
            print(f"✅ Bin {i}: matches (waste = {actual:.6f})")


if __name__ == '__main__':
    #run_best_fit_with_1500000_items()
    #test_random_insert_remove()
    #test_best_fit_10_items()
    test_best_fit_20_items()