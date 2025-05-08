
#tim sort wants us to divide our given list into "runs"
#runs are already sorted sublists
#each "Run" can be either increasing or decreasing
#for example:

#[7,1,2,3,4,12,8,9,10,9,8,7]
#this should result in the run list being:
#[[7,1],[2,3,4,12],[8,9,10],[9,8,7]]
from collections import deque #to use as a stack

def get_runs(nums:list[int]):
    if len(nums) == 0:
        return []
    elif len(nums) == 1:
        return [[nums[0]]]
    
    runs = []#list of runs we're going to return
    curr_run = []
    increasing = True
    decreasing = True
    prev = nums[0]
    

    def update_current_run(i) -> int:
        curr_run.append(prev)
        return nums[i]


    for i in range(1,len(nums)):
        #TODO handle case for when prev and num[i] are equal
        if nums[i] == prev:
            prev = update_current_run(i)
        elif nums[i] > prev and increasing:
            prev = update_current_run(i)
            decreasing = False
        elif nums[i] < prev and decreasing:
            prev = update_current_run(i)
            increasing = False
        else:
            prev = update_current_run(i)
            runs.append(curr_run)
            curr_run = []
            increasing = True
            decreasing = True

    #if we exit the loop and curr_run isn't empty, then we should append it to runs
    #otherwise we wont get the last run
    #example:[7,1,2,3,4,12,8,9,10,9,8,7]
    #expected: [[7, 1], [2, 3, 4, 12], [8, 9, 10], [9, 8, 7]]
    #actual result: [[7, 1], [2, 3, 4, 12], [8, 9, 10]]

    #we are always skipping the last element, and the last element will always either be apart of the previous run
    #or be in it's own run
    curr_run.append(prev)
    runs.append(curr_run)


    for i in range(len(runs)):
        if len(runs[i]) > 1 and runs[i][0] > runs[i][-1]:
            runs[i] = runs[i][::-1]
    return runs


def merge_runs(run1,run2):
    # If a run is in decreasing order, reverse it first
    '''
    if len(run1) > 1 and run1[0] > run1[1]:
        run1 = run1[::-1]
    if len(run2) > 1 and run2[0] > run2[1]:
        run2 = run2[::-1]
    '''
    

    result = []
    i = 0
    j = 0

    while i < len(run1) and j < len(run2):
        if run1[i] <= run2[j]:
            result.append(run1[i])
            i+=1
        else:
            result.append(run2[j])
            j+=1

    #same deal, once we finish the loop, one of the two runs will be left with elements not in result
    #so we have to add them in
    result.extend(run1[i:]) #just bringing the last few elements on
    result.extend(run2[j:])
    return result
    
def tim_sort(nums: list[int]):
    runs = get_runs(nums) #run decomposition of nums, should be a nested list
    #example:
    #nums = [7, 1, 2, 3, 4, 12, 8, 9, 10, 9, 8, 7]
    #expected = [[7, 1], [2, 3, 4, 12], [8, 9, 10], [9, 8, 7]]
    run_stack = []
    while len(runs) != 0:
        run = runs.pop()
        run_stack.append(run) #add each run to the stack
        while True:
            h = len(run_stack)
            if h >= 4:
                r4 = len(run_stack[-4])
            if h >= 3:
                r3 = len(run_stack[-3])
            if h >= 2:
                r2 = len(run_stack[-2])
                r1 = len(run_stack[-1])
            else: 
                break #should only happen if h is less than 2

        
            if h >= 3 and r1>r3:
                run2 = run_stack[-2]
                run3 = run_stack[-3]
                run_stack[-2] = merge_runs(run2,run3)
                del run_stack[-3]
            elif h >= 2 and r1>=r2:
                run1 = run_stack.pop()
                run2 = run_stack.pop()
                result = merge_runs(run1,run2)
                run_stack.append(result)
            elif h >= 3 and r1+r2>=r3:
                run1 = run_stack.pop()
                run2 = run_stack.pop()
                result = merge_runs(run1,run2)
                run_stack.append(result)
            elif h >= 4 and r2+r3>=r4:
                run1 = run_stack.pop()
                run2 = run_stack.pop()
                result = merge_runs(run1,run2)
                run_stack.append(result)
            else:
                break

    h = len(run_stack)
    while h > 1:
        run1 = run_stack.pop()
        run2 = run_stack.pop()
        result = merge_runs(run1,run2)
        run_stack.append(result)
        h = len(run_stack)
    
    nums[:] = run_stack[0] if run_stack else []
