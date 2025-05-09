import random
from zipzipbf import ZipZipTreeBF
from best_fit import best_fit  # Adjust import if needed

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

if __name__ == '__main__':
    run_best_fit_with_1500000_items()