import zipzipbf
from tim_sort import tim_sort

def best_fit(items: list[float], assignment: list[int], free_space: list[float]):
    # Convert items and free_space to Decimal for precise calculations

    tree = zipzipbf.ZipZipTreeBF(len(items))
    bin_index = 0
    tree.insert((1.0,0), 0)  # Use Decimal for initial free space
    free_space.append(1.0)

    for i, item in enumerate(items):
        bin_found = tree.allocate_bin(item, bin_index)
        if bin_found > len(free_space) - 1:
            # Allocate a new bin and update free_space
            free_space.append(1.0 - item)
            bin_index += 1
        else:
            # Deduct the space from the found bin
            free_space[bin_found] -= item
        
        # Assign the bin index to the item
        assignment[i] = bin_found

        # Print debugging information
        #print(f"\n\ncurrent item: {item}")
        #tree.print_tree()
    return tree

def best_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
    tim_sort(items)
    items = items[::-1]
    best_fit(items,assignment,free_space)