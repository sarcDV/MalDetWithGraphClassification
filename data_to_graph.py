import os, sys
import numpy as np 
import networkx as nx
import pandas as pd
import h5py
import hashlib
import  warnings
warnings.filterwarnings('ignore')
## ---------------------------------------------------
class BinaryPairListConverter:
    def __init__(self, file):
        self.file = file

    def bin2pair(self):
        with open(self.file, 'rb') as binary_file:        
            data = binary_file.read()
        d = np.frombuffer(data, dtype=np.uint8) 
        if len(d) % 2 != 0:
            # If the length is odd, add a single zero at the end of the array
            d = np.append(d, 0)

        # Reshape the array to have 2 rows and N columns
        # d = d.reshape(-1, int(len(d) / 2))
        # Reshape the array to have 2 columns and N rows
        d = d.reshape(int(len(d) / 2), -1)
        return d
    

class PairListToGraph:
    def __init__(self, array2N):
        self.array2N = array2N

    def pair2graph(self):    
        # Create an empty graph
        G = nx.Graph()
        for i in range(0, self.array2N.shape[0]):
            G.add_edge(self.array2N[i,0],self.array2N[i,1] )
            
        return G   
    
class Binary2Graph:
    def __init__(self, file):
        self.file = file

    def bin2graph(self):
        converter = BinaryPairListConverter(self.file)
        pairs = converter.bin2pair()
        arrtograph = PairListToGraph(pairs)
        G = arrtograph.pair2graph()
        c_graph, c_nodes = nx.dedensify(G, threshold=2)
        return c_graph

def main():
    Data2Graph(sys.argv[1], sys.argv[2])
    return 

def Data2Graph(folder, csvfile):
    """
    Modifications to be made:
    1. Convert all files in the folder and save them in HDF5 format.
    """
    list_files = os.listdir(folder)
    path_ = os.path.join(os.getcwd(), os.path.dirname(folder))
    dflabel = pd.read_csv(csvfile)
    print(dflabel)
    # Create an HDF5 file to store the data
    hdf5_file = "graph_data.h5"
    with h5py.File(hdf5_file, "a") as f:
        # Loop through each file
        for file in list_files:
            file_ = os.path.join(path_, file)
            filename = os.path.basename(file_)
            print(f"Processing {filename}")
            with open(file_, 'rb') as binary_file:        
                data = binary_file.read()
            # Convert binary data to graph
            converter = Binary2Graph(file_)
            graph_ = converter.bin2graph()
            tdf = nx.to_pandas_edgelist(graph_)
            
            # Filter rows where any element (string) has length > 3
            tdf = tdf[tdf.applymap(lambda x: len(x) <= 3 if isinstance(x, str) else True).all(axis=1)]
    
            # Convert columns to appropriate data types
            tdf["source"] = tdf["source"].astype("uint8")
            tdf["target"] = tdf["target"].astype("uint8")
            
            # Append tdf to the HDF5 file
            group_name = os.path.splitext(filename)[0]
            f.create_group(group_name)
            f[group_name].create_dataset("tdf", data=tdf.to_records(index=False))
            
            # Add label to the group based on filename matching with dflabel
            
            md5_hash = hashlib.md5(data).hexdigest()
            matching_row = dflabel[dflabel["md5"] == md5_hash]
            print(matching_row)
            if not matching_row.empty:
                list_value = matching_row["list"].iloc[0]
                label = 0 if list_value.lower() in ["Whitelist", "whitelist"] else 1
                f[group_name].attrs["label"] = label

    print(f"All data saved to {hdf5_file}")

if __name__ == '__main__':
        main()
