import os, sys, glob, shutil
import numpy as np 
import networkx as nx
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
    Data2Graph(sys.argv[1])
    return 

def Data2Graph(folder):
    """modifiche da fare: get the filename and replace the output
       . 1 provare a convertire tutti i file in una cartella e salvarli in formato hdf5
       
    """
    list_files=os.listdir(folder)
    path_ = os.path.join(os.getcwd(), os.path.dirname(folder))
    # Loop through each file
    for file in list_files:
        file_ = os.path.join(path_, file)
        # get filename:
        filename = os.path.basename(file_)
        converter = Binary2Graph(file_)
        graph_ = converter.bin2graph()
       
    

if __name__ == '__main__':
        main()
