from math import isclose
import zipzipff

def first_fit(items: list[float], assignment: list[int], free_space: list[float]):

    tree = zipzipff(len(items))
    bin_index = 0
    tree.insert(0,1.0)
    free_space.append(1.0)

    for i,item in enumerate(items):
        bin_found = tree.allocate_bin(item,bin_index)
        if(bin_found > len(free_space)):
            free_space.append(1.0-item)

        assignment[i] = bin_index
        free_space[bin_found] -= item


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