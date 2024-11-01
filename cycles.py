import networkx as nx
import matplotlib.pyplot as plt
import scipy
import itertools
from algorithm import algo

def isRotation(tuple1, tuple2):
    n = len(tuple1)
    for s in range(len(tuple1)):
        sol = True
        for i in range(len(tuple1)):
            if tuple1[i] != tuple2[(i+s)%(n)]:
                sol = False 
        if sol:
            return True 
    return False 

def isEq(tuple1, tuple2):
    c1 = tuple1[:6]
    c2 = tuple2[:6]
    r1 = tuple1[-6:]
    r2 = tuple2[-6:]
    for s in range(len(tuple1)):
        sol = True
        for i in range(6):
            if c1[i] != c2[(i+s)%(6)] or r1[i] != r2[(i+s)%(6)]:
                sol = False 
        if sol:
            return True 
    return False 
    


def isRotationD(tuple1, tuple2):
    n = len(tuple1)
    if tuple1[-1] != tuple2[-1]:
        return False 
    else:
        for s in [3]:
            sol = True
            for i in range(len(tuple1)-1):
                if tuple1[i] != tuple2[(i+s)%(n)]:
                    sol = False 
            if sol:
                return False #True 
    return False 

def generateWeights(length, readability):
    result = []
    seen = set()  # Use a set to track unique combinations

    for combination in itertools.product(range(1, readability + 1), repeat=length):
        # Check if the combination or any of its rotations are already seen
        if not any(isRotation(combination, existing) for existing in seen):
            result.append(combination)  # Add the new unique combination
            seen.add(combination)  # Add to seen set to track rotations
    #print(len(result))
    return result

# Create a directed graph
G = nx.DiGraph()

# Adding nodes: Even integers for sources, odd integers for targets
# Source nodes (even) and target nodes (odd) inferred from the image
source_nodes = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28]
target_nodes = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29]

# Add nodes to the graph
G.add_nodes_from(source_nodes, bipartite=0)  # Set of sources
G.add_nodes_from(target_nodes, bipartite=1)  # Set of targets

edges =[(0,1), (2,1), (2,3), (4, 3), (4,5), (0, 5), (0,7) , (6, 1), (6,7), (6,9), (8,7), (8,9), ( 10, 1), (2,11), (10, 11), (10,13), (12, 11), (12,13), (2,15), (14,3), (14,15), (16, 15), (14, 17), (16, 17), (18, 3), (4, 19), (18,19), (18, 21), (20, 19), (20,21), (4, 23), (22, 5), (22,23), (22,25), (24,23), (24,25), (26, 5), (0,27), (26,27), (26, 29), (28, 27), (28,29)]

G.add_edges_from(edges)

ext = [(0,7,2), (8,1,1), (2,9,3), (10,3,1), (4,11,2), (6,5,1)]

C6 = nx.DiGraph() 
C6.add_nodes_from(source_nodes[:3], bipartite=0)  # Set of sources
C6.add_nodes_from(target_nodes[:3], bipartite=1)  # Set of targets
#C6.add_edges_from(edges[:6])
C6.add_weighted_edges_from([(0,1,1), (2,1,2), (2,3,1), (4, 3,2), (4,5,1), (0, 5,2)]) #+[(6,5), (6,7), (0,7)])
#C6.add_weighted_edges_from(ext)

e = [(0,1), (2,1), (2,3), (4, 3), (4,5), (0, 5)]

def feasibleWeights(graph, edges, readability):
     n = graph.number_of_edges()
     weights = generateWeights(n, readability)
     #print(weights)
     for w in weights: 
         #print(w)
         d = {edges[i]: w[i] for i in range(n)}
         nx.set_edge_attributes(graph, d, name="weight")
         x = algo(graph, readability)
         print(d, x)
         if x:
             with open('newc6.txt', 'a') as file: 
                 file.write(f"Weights:{w}\n")
          

if __name__=="__main__":
    #feasibleWeights(C6, 3)
    print(0)