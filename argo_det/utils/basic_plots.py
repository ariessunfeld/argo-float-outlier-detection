import numpy as np
import matplotlib.pyplot as plt

def plot_variable_vs_depth(data, variable):
    depth = data['depth']
    values = data[variable]

    # Plot
    plt.figure(figsize=(8, 6))
    plt.plot(values[0, :], depth[0, :], label=variable.capitalize())
    plt.gca().invert_yaxis()  # Depth increases downwards
    plt.xlabel(f"{variable.capitalize()} (units)")
    plt.ylabel("Depth")
    plt.title(f"{variable.capitalize()} vs Depth")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_variable_vs_time(data, variable):
    time = data['time']
    values = data[variable]
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(time, values[:, 0], '-o', label=variable.capitalize())  # Example for profile 0
    plt.xlabel("Time (Julian Days)")
    plt.ylabel(f"{variable.capitalize()} (units)")
    plt.title(f"{variable.capitalize()} vs Time")
    plt.legend()
    plt.grid(True)
    plt.show()
