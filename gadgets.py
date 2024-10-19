import networkx as nx
#import matplotlib.pyplot as plt
#import scipy
import itertools
from algorithm import algo
import pickle  # Used to store state as binary data
import os 

# Create a directed graph
G = nx.DiGraph()

# Adding nodes: Even integers for sources, odd integers for targets
# Source nodes (even) and target nodes (odd) inferred from the image
source_nodes = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28]
target_nodes = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29]

#find all the possible weight decomposition of induced subgraph of size n, and then based on this, find the possible ones for n+1
d = {(0, 1): 1, (2, 1): 2, (2, 3): 1, (4, 3): 2, (4, 5): 1, (0, 5): 2, (0, 7): 1, (6, 1): 1, (6, 7): 1, (8, 7): 1, (6, 9): 1, (8, 9): 1, (10, 1): 1, (2, 11): 1, (10, 11): 1, (10, 13): 1, (12, 11): 1, (12, 13): 1, (2, 15): 1, (14, 3): 1, (14, 15): 1, (16, 15): 1, (14, 17): 1, (16, 17): 1, (18, 3): 1, (4, 19): 1, (18, 19): 1, (18, 21): 2, (20, 19): 3, (20, 21): 2, (4, 23): 3, (22, 5): 3, (22, 23): 1, (24, 23): 1, (22, 25): 1, (24, 25): 1, (26, 5): 1, (0, 27): 3, (26, 27): 3, (26, 29): 2, (28, 27): 2, (28, 29): 1} 


# Add nodes to the graph
G.add_nodes_from(source_nodes, bipartite=0)  # Set of sources
G.add_nodes_from(target_nodes, bipartite=1)  # Set of targets

edgesg =[(0,1), (2,1), (2,3), (4, 3), (4,5), (0, 5), (0,7) , (6, 1), (6,7), (8,7),(6,9), (8,9), ( 10, 1), (2,11), (10, 11), (10,13), (12, 11), (12,13), (2,15), (14,3), (14,15), (16, 15), (14, 17), (16, 17), (18, 3), (4, 19), (18,19), (18, 21), (20, 19), (20,21), (4, 23), (22, 5), (22,23), (24,23), (22,25), (24,25), (26, 5), (0,27), (26,27), (26, 29), (28, 27), (28,29)]

G.add_edges_from(edgesg)

weightsC = [(1,2,1,2,1,2)]#, 1,1,1,3,3,2, 3,3,1,1,1,1, 1,1,1,3,3,2, 3,3,1,1,1,1, 1,1,1,3,3,2, 3,3,1,1,1)] #[(1, 1, 2, 1, 1, 3),(1, 1, 2, 3, 1, 2),(1, 1, 2, 3, 1, 3),(1, 1, 3, 1, 1, 3),(1, 1, 3, 1, 2, 3),(1, 1, 3, 2, 1, 3),(1, 2, 1, 2, 1, 3),(1, 2, 1, 3, 1, 3),(1, 2, 2, 3, 1, 3),(1, 3, 2, 1, 3, 2)]

weightsG = (1,2,1,2,1,2, 1,1,1,3,3,2, 3,3,1,1,1,1, 1,1,1,3,3,2, 3,3,1,1,1,1, 1,1,1,3,3,2, 3,3,1,1,1,2)

C6 = nx.DiGraph() 
C6.add_nodes_from(source_nodes[:3], bipartite=0)  # Set of sources
C6.add_nodes_from(target_nodes[:3], bipartite=1)  # Set of targets
C6.add_edges_from(edgesg[:6])


def isRotation(tuple1, tuple2, rotations):
    n = len(tuple1)
    for s in rotations : #range(len(tuple1)):#[6,12,18,24, 30]
        sol = True
        for i in range(len(tuple1)):
            if tuple1[i] != tuple2[(i+s)%(n)]:
                sol = False 
        if sol:
            return True 
    return False 


def generateWeightsG(length, readability, allowed_tuples):
    allowed_set = set(allowed_tuples)  # Convert to a set for faster lookup
    for allowed in allowed_set:
        for remaining in itertools.product(range(1, readability + 1), repeat=length-6):#length - 6):
            yield allowed + remaining

def equivalentGadgets(w1, w2):
    c1 = w1[:6]
    r1 = w1[-len(w1) +6 :]
    c2 = w1[:6]
    r2 = w1[-len(w1) +6 :]
    for i in range(5):
        sol = True 
        if not isRotation(c1, c2, [i]) or not isRotation(r1, r2, [6*i]):
            sol = False 
        if sol:
            return True
    return False 


def areWeightsFeasible(graph, edges, readability, weights):
    n = graph.number_of_edges()
    d = {edges[i]: weights[i] for i in range(n)}
    #d = weights
    nx.set_edge_attributes(graph, d, name="weight")
    #print(d)
    x=algo(graph, readability)
    print(d,x)
    return x 
        
def feasibleWeights(graph, edges, readability):
    n = graph.number_of_edges()
     #weights = generateWeightsG(n, readability, weightsC)
     #print(weights)
    i = 0
    if os.path.exists("checkpoint.pkl"):
            with open("checkpoint.pkl", 'rb') as f:
                checkpoint = pickle.load(f)
                i = checkpoint['i']  # Resume from saved index
                print(f"Resuming from checkpoint at iteration {i}")
    else:
        checkpoint = {'i': 0}
    for w in generateWeightsG(n, readability, weightsC): 
        """ 
        d = {edges[i]: w[i] for i in range(n)}
        #d = {list(graph.edges)[i]: w[i] for i in range(n)}
        nx.set_edge_attributes(graph, d, name="weight")
        #print(d)
        x=algo(graph, readability)
        print(d,x)
        """ 
        
        if i < checkpoint['i']:
            i += 1  # Skip already processed iterations
            continue
        x = areWeightsFeasible(graph, edges, readability, w)
        if x:
            "inside de if"
            with open('results.txt', 'a') as file: 
                file.write(f"Weights:{w}\n")
        i += 1

        if i % 100 == 0:
            checkpoint['i'] = i
            with open("checkpoint.pkl", 'wb') as f:
                pickle.dump(checkpoint, f)
            print(f"Checkpoint saved at iteration {i}")

        if i > 25210:
            break
     
          

if __name__=="__main__":
    #feasibleWeights(C6, 3)
    #generateWeightsG(42,3, weightsC)
    feasibleWeights(G,edgesg, 3)