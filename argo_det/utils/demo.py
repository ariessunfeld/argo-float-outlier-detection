from pathlib import Path

from argo_det.utils.ingestion import load_argo_data, print_variable_data
from argo_det.utils.basic_plots import plot_variable_vs_depth, plot_variable_vs_time
from argo_det.utils.basic_plots_pg import plot_variable_vs_depth_pg, plot_variable_vs_time_pg

if __name__ == '__main__':
    filepath = Path(__file__).parent.parent.parent / 'data' / '5906296_Sprof.nc'

    # Load data
    argo_data = load_argo_data(filepath)

    print_variable_data(argo_data, 'temperature')

    # Plot temperature vs depth
    #plot_variable_vs_depth(argo_data, 'temperature')
    plot_variable_vs_depth_pg(argo_data, 'temperature')

    # Plot temperature vs time
    #plot_variable_vs_time(argo_data, 'temperature')
    plot_variable_vs_time_pg(argo_data, 'temperature')
