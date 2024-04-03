import os, sys, glob, shutil

import numpy as np 
from math import ceil, sqrt
from skimage.feature import graycomatrix
import  warnings
import networkx as nx
import matplotlib.pyplot as plt

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
        converter = BinaryPairListConverter(file)
        pairs = converter.bin2pair()
        arrtograph = PairListToGraph(pairs)
        G = arrtograph.pair2graph()
        # print(G.number_of_edges())
        c_graph, c_nodes = nx.dedensify(G, threshold=2)
        # print(c_graph.number_of_edges())
        # nx.write_gexf(c_graph, "file.gexf")
        return c_graph

def main():
    Data2Graph(sys.argv[1])
    return 

def Data2Graph(folder):
    """modifiche da fare: get the filename and replace the output
       . 1 provare a convertire tutti i file in una cartella e salvarli in formato hdf5
       
    """
    list_files=os.listdir(folder)
    # Loop through each file
    for file in list_files:
        # get filename:
        filename = os.path.basename(file)
        converter = Binary2Graph(file)
        graph_ = converter.bin2graph()
       
    

if __name__ == '__main__':
        main()
