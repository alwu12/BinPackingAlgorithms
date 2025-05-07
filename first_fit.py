from math import isclose
from decimal import Decimal, getcontext
import zipzipff

getcontext().prec = 45



def first_fit(items: list[float], assignment: list[int], free_space: list[float]):
    # Convert items and free_space to Decimal for precise calculations

    tree = zipzipff.ZipZipTreeFF(len(items))
    bin_index = 0
    tree.insert(0, 1.0)  # Use Decimal for initial free space
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
        #print(f"current item: {item}")
        #tree.print_tree()


'''
def first_fit(items: list[float], assignment: list[int], free_space: list[float]):
    items = [Decimal(item) for item in items]
    tree = zipzipff.ZipZipTreeFF(len(items))
    bin_index = 0
    tree.insert(0,Decimal('1.0'))
    free_space.append(1.0)

    for i,item in enumerate(items):
        bin_found = tree.allocate_bin(item,bin_index)
        if(bin_found > len(free_space)-1):
            free_space.append(Decimal('1.0')-item)
            bin_index+=1

        
        #print(f"binfound: {bin_found}")
        #print(f"len of freespace: {len(free_space)}")
        else:
            free_space[bin_found] -= item
        assignment[i] = bin_found
        
        print(f"current item: {item}")
        tree.print_tree()
'''

    #items: the items to assign to the bins
# 	assignment: the assignment of the ith item to the jth bin for all i items.
# 	            bin numbers start from 0.
# 	            assume len(assignment) == len(items).
# 	            you should not add any new elements to this list.
# 	            you must modify this list's elements to indicate the assignment.
# 	            see comment below for first-fit decreasing and for best-fit decreasing.
#
# 	free_space: the amount of space left in the jth bin for all j bins created by the algorithm.
# 	            you should add one element for each bin that the algorithm creates.
# 	            when the function returns, this should indicate the final free space available in each bin.