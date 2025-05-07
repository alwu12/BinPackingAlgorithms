# Example file: next_fit.py

# explanations for member functions are provided in requirements.py


#we need an epsilon because floating point arithmetic is not exact
#if item <= free_space[bin_index]
#can fail even if the values should be equal mathematically — 
#due to tiny rounding errors like 0.29999999999999993 instead of 0.3

#An epsilon (EPS) is a tiny number (like 1e-11) 
#that you use to allow a small margin of error in comparisons:

from math import isclose

def next_fit(items: list[float], assignment: list[int], free_space: list[float]):
	#EPS = 4e-11
	bin_index = 0
	free_space.append(1.0)

	for i,item in enumerate(items):
		#if item <= free_space[bin_index] + EPS:
		if item < free_space[bin_index] or isclose(item,free_space[bin_index]):
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