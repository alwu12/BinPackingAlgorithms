from benchmark_get_averages import *

import matplotlib.pyplot as plt
import numpy as np



BIN_PACKING_ALGORITHMS = [
    #'next_fit'
    #'first_fit'
    'first_fit_decreasing'
    #'best_fit'
    #'best_fit_decreasing'
]



def plot_alg(data, label, markersize, color, legend_handles):
    #data is dataset of size+time running
    #label is which permutation
    #markersize is how big we want our dots to be
    #color is color of the dot and line
    #basex and basey refer to the base of the logarithm used
    x_vals = []
    y_vals = []
    print(f'data: {data}')
    for x, y in sorted(data.items()):
        x_vals.append(x)
        y_vals.append(y)

    

    
    # Plot all points at once to avoid duplicate legends
    plt.loglog(x_vals, y_vals, '.', label=label, markersize=markersize, color=color)
    #plt.loglog(x_vals, y_vals, '-', color=color)  # Line connecting the dots
    

    x = np.array(x_vals)
    y = np.array(y_vals)
    x_fit = x[0:]#this ignores the first 5 values when making our line of best fit
    y_fit = y[0:]
    logx = np.log2(x_fit)
    logy = np.log2(y_fit)
    m, b = np.polyfit(logx, logy, 1)


    equation = f"y = {m:.5f} * log N + {b:.2f}"
    

    plt.loglog(x_fit, 2 ** (m * logx + b), color=color)
    legend_handles[label] = plt.Line2D([0], [0], marker='o', color='red', label=f"{label} ({equation})", markersize=6, linestyle='None')
    
def plot_algorithm(data, algorithm_name):
    # Plot for different permutations
    legend_handles = {}
    plot_alg(data[algorithm_name], algorithm_name, 6, 'red',legend_handles)
    

    # Set the plot scale and labels
    plt.xscale('log', base=2)
    plt.yscale('log', base=2)
    plt.xlabel("Input Size")
    plt.ylabel("Waste")
    plt.yticks()
    plt.title(f"{algorithm_name.replace('_', ' ').title()} Performance")
    #plt.legend(handles=[legend_handles['ALMOST_SORTED'], legend_handles['ALTERNATING'], legend_handles['UNIFORMLY_DISTRIBUTED']])
    plt.legend(handles=list(legend_handles.values()))
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    data = return_all_data()
    for i in BIN_PACKING_ALGORITHMS:
        plot_algorithm(data, i)