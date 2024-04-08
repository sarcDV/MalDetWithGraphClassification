import torch
from torch.utils.data import Dataset, DataLoader
from torch_geometric.data import Data

class MyGraphDataset(Dataset):
    def __init__(self, h5_file_path):
        # Store the path to your H5 file
        self.h5_file_path = h5_file_path

    def __len__(self):
        # Return the total number of dataframes (assuming each dataframe corresponds to a graph)
        # You can adapt this based on your actual data
        return 200000

    def __getitem__(self, idx):
        # Load the dataframe at the specified index from the H5 file
        # Convert it to a graph and return the graph data object
        graph_data = self._load_dataframe_and_convert_to_graph(idx)
        return graph_data

    def _load_dataframe_and_convert_to_graph(self, idx):
        # Load the dataframe at the given index from the H5 file
        # Assuming you have a function to load dataframes from your H5 file
        dataframe = load_dataframe_from_h5(self.h5_file_path, idx)

        # Extract 'source' and 'target' columns
        source_nodes = dataframe['source'].values
        target_nodes = dataframe['target'].values

        # Create a PyTorch Geometric Data object
        edge_index = torch.tensor([source_nodes, target_nodes], dtype=torch.long)
        x = torch.zeros(len(source_nodes), 1)  # Node features (you can adapt this)
        graph_data = Data(x=x, edge_index=edge_index)

        return graph_data

# Example usage:
h5_file_path = 'path/to/your/h5_file.h5'
dataset = MyGraphDataset(h5_file_path)
batch_size = 32  # Adjust as needed
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

for batch in dataloader:
    # Your training/validation loop goes here
    pass

import h5py

def count_groups(h5_file_path):
    try:
        with h5py.File(h5_file_path, 'r') as h5_file:
            num_groups = len(h5_file.keys())
            return num_groups
    except Exception as e:
        print(f"Error reading HDF5 file: {e}")
        return None

# Example usage:
h5_file_path = 'path/to/your/h5_file.h5'
num_groups = count_groups(h5_file_path)

if num_groups is not None:
    print(f"Number of groups in the HDF5 file: {num_groups}")
else:
    print("Unable to read the HDF5 file.")
