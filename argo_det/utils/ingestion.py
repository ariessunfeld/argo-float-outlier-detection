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

# def load_argo_data(filepath):
#     dataset = nc.Dataset(filepath, 'r')

#     # Extract depth (N_LEVELS), time (JULD), and variables, then clean them
#     depth = clean_data_2(dataset.variables['PRES'][:])  # Depth/Pressure
#     time = clean_data_2(dataset.variables['JULD'][:])   # Time (in Julian days)
    
#     # Extract variables (temperature, salinity, oxygen, nitrate, pH) and clean them
#     temperature = clean_data_2(dataset.variables['TEMP'][:])
#     salinity = clean_data_2(dataset.variables['PSAL'][:])
#     oxygen = clean_data_2(dataset.variables['DOXY'][:])
#     nitrate = clean_data_2(dataset.variables['NITRATE'][:])
#     ph = clean_data_2(dataset.variables['PH_IN_SITU_TOTAL'][:])
    
#     # Extract quality control flags (optional, not cleaning as they are categorical)
#     temp_qc = dataset.variables['TEMP_QC'][:]
#     sal_qc = dataset.variables['PSAL_QC'][:]
    
#     return {
#         'depth': depth,
#         'time': time,
#         'temperature': temperature,
#         'salinity': salinity,
#         'oxygen': oxygen,
#         'nitrate': nitrate,
#         'ph': ph,
#         'temp_qc': temp_qc,
#         'sal_qc': sal_qc,
#     }


def load_argo_data(filepath):
    dataset = nc.Dataset(filepath, 'r')

    print(f'Loading file: {filepath}')

    def safe_extract_variable(var_name, default=None):
        """Safely extract a variable from the dataset, returning a default value if the variable is missing."""
        try:
            return clean_data_2(dataset.variables[var_name][:])
        except KeyError:
            print(f"Warning: {var_name} not found in the dataset. Using default value.")
            return default

    def safe_extract_qc_variable(var_name, default=None):
        """Safely extract a quality control variable, returning a default value if the variable is missing."""
        try:
            return dataset.variables[var_name][:]
        except KeyError:
            print(f"Warning: QC variable {var_name} not found in the dataset. Using default value.")
            return default

    # Safely extract depth (N_LEVELS), time (JULD), and variables
    depth = safe_extract_variable('PRES', default=None)  # Depth/Pressure
    time = safe_extract_variable('JULD', default=None)   # Time (in Julian days)

    # Safely extract variables (temperature, salinity, oxygen, nitrate, pH)
    temperature = safe_extract_variable('TEMP', default=None)
    salinity = safe_extract_variable('PSAL', default=None)
    oxygen = safe_extract_variable('DOXY', default=None)
    nitrate = safe_extract_variable('NITRATE', default=None)
    ph = safe_extract_variable('PH_IN_SITU_TOTAL', default=None)

    # Safely extract quality control flags (optional)
    temp_qc = safe_extract_qc_variable('TEMP_QC', default=None)
    sal_qc = safe_extract_qc_variable('PSAL_QC', default=None)

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
