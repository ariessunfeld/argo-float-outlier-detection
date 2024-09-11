import numpy as np
import netCDF4 as nc

def clean_data(array):
    """
    Replaces non-numeric or invalid values (e.g., '--') with NaN.
    This function is applied to each variable in the dataset.
    """
    # Convert array to float, replacing '--' with NaN
    array = np.where(array == '--', np.nan, array).astype(np.float64)
    return array

def clean_data_2(array):
    array = clean_data(array)
    array = np.where(array == 99999, np.nan, array)
    return array

def load_argo_data(filepath):
    dataset = nc.Dataset(filepath, 'r')

    # Extract depth (N_LEVELS), time (JULD), and variables, then clean them
    depth = clean_data_2(dataset.variables['PRES'][:])  # Depth/Pressure
    time = clean_data_2(dataset.variables['JULD'][:])   # Time (in Julian days)
    
    # Extract variables (temperature, salinity, oxygen, nitrate, pH) and clean them
    temperature = clean_data_2(dataset.variables['TEMP'][:])
    salinity = clean_data_2(dataset.variables['PSAL'][:])
    oxygen = clean_data_2(dataset.variables['DOXY'][:])
    nitrate = clean_data_2(dataset.variables['NITRATE'][:])
    ph = clean_data_2(dataset.variables['PH_IN_SITU_TOTAL'][:])
    
    # Extract quality control flags (optional, not cleaning as they are categorical)
    temp_qc = dataset.variables['TEMP_QC'][:]
    sal_qc = dataset.variables['PSAL_QC'][:]
    
    return {
        'depth': depth,
        'time': time,
        'temperature': temperature,
        'salinity': salinity,
        'oxygen': oxygen,
        'nitrate': nitrate,
        'ph': ph,
        'temp_qc': temp_qc,
        'sal_qc': sal_qc,
    }



def print_variable_data(data, variable):
    depth = data['depth']
    values = data[variable]

    print(f"\nVariable: {variable}")
    print(f"Depth data (first profile):\n{depth[0, :]}")
    print(f"Values (first profile):\n{values[0, :]}")
