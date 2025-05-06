# Example file: next_fit.py

# explanations for member functions are provided in requirements.py

def next_fit(items: list[float], assignment: list[int], free_space: list[float]):

	bin_index = 0
	free_space.append(1.0)

	for i,item in enumerate(items):
		if item <= free_space[bin_index]:
			free_space[bin_index] -= item
			assignment.append(bin_index)
		else:
			bin_index+=1
			free_space.append(1 - item)
			assignment[i] = bin_index

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