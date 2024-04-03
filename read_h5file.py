import h5py

# Specify the path to your HDF5 file
hdf5_file = "graph_data.h5"

# Open the HDF5 file in read mode
with h5py.File(hdf5_file, "r") as f:
    # List all groups (corresponding to filenames)
    group_names = list(f.keys())
    print(f"Available groups (filenames): {group_names}")

    # Example: Access data for a specific group (replace 'your_group_name' with an actual group name)
    your_group_name = "1122"
    if your_group_name in f:
        dataset = f[your_group_name]["tdf"]  # Access the dataset within the group
        data = dataset[:]  # Load the data into a numpy array
        label = f[your_group_name].attrs.get("label", None)  # Get the label attribute
        print(f"Data for group '{your_group_name}':\n{data}")
        print(f"Label for group '{your_group_name}': {label}")
    else:
        print(f"Group '{your_group_name}' not found in the HDF5 file.")
