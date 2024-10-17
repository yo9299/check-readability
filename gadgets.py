import networkx as nx
#import matplotlib.pyplot as plt
#import scipy
import itertools
from algorithm import algo

weightsC = [(1, 1, 2, 1, 1, 3),(1, 1, 2, 3, 1, 2),(1, 1, 2, 3, 1, 3),(1, 1, 3, 1, 1, 3),(1, 1, 3, 1, 2, 3),(1, 1, 3, 2, 1, 3),(1, 2, 1, 2, 1, 3),(1, 2, 1, 3, 1, 3),(1, 2, 2, 3, 1, 3),(1, 3, 2, 1, 3, 2)]

weightsG = (1,2,1,2,1,2, 1,1,1,3,3,2, 3,3,1,1,1,1, 1,1,1,3,3,2, 3,3,1,1,1,1, 1,1,1,3,3,2, 3,3,1,1,1,1)

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


def generateWeights(length, readability, rotations):
    result = []
    seen = set()  # Use a set to track unique combinations

    for combination in itertools.product(range(1, readability + 1), repeat=length):
        # Check if the combination or any of its rotations are already seen
        if not any(isRotation(combination, existing, rotations) for existing in seen):
            result.append(combination)  # Add the new unique combination
            seen.add(combination)  # Add to seen set to track rotations
    #print(len(result))
    return result

def generateWeightsGadget(length, readability):
    result = []
    seen = set()  # Use a set to track unique combinations

    for combination in itertools.product(range(1, readability + 1), repeat=length):
        # Check if the combination or any of its rotations are already seen
        if not any(equivalentGadgets(combination, existing) for existing in seen):
            #result.append(combination)  # Add the new unique combination
            seen.add(combination)  # Add to seen set to track rotations
            print(seen)
    #print(len(result))
    return seen

def generateWeightsG(length, readability, allowed_tuples):
    allowed_set = set(allowed_tuples)  # Convert to a set for faster lookup
    for allowed in allowed_set:
        for remaining in itertools.product(range(1, readability + 1), repeat=length - 6):
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
# Create a directed graph
G = nx.DiGraph()

# Adding nodes: Even integers for sources, odd integers for targets
# Source nodes (even) and target nodes (odd) inferred from the image
source_nodes = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28]
target_nodes = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29]

# Add nodes to the graph
G.add_nodes_from(source_nodes, bipartite=0)  # Set of sources
G.add_nodes_from(target_nodes, bipartite=1)  # Set of targets

edgesg =[(0,1), (2,1), (2,3), (4, 3), (4,5), (0, 5), (0,7) , (6, 1), (6,7), (8,7),(6,9), (8,9), ( 10, 1), (2,11), (10, 11), (10,13), (12, 11), (12,13), (2,15), (14,3), (14,15), (16, 15), (14, 17), (16, 17), (18, 3), (4, 19), (18,19), (18, 21), (20, 19), (20,21), (4, 23), (22, 5), (22,23), (24,23), (22,25), (24,25), (26, 5), (0,27), (26,27), (26, 29), (28, 27), (28,29)]

G.add_edges_from(edgesg)


C6 = nx.DiGraph() 
C6.add_nodes_from(source_nodes[:3], bipartite=0)  # Set of sources
C6.add_nodes_from(target_nodes[:3], bipartite=1)  # Set of targets
C6.add_edges_from(edgesg[:6])


def feasibleWeights(graph, edges, readability):
    n = graph.number_of_edges()
     #weights = generateWeightsG(n, readability, weightsC)
     #print(weights)
    i = 0
    for w in generateWeightsG(n, readability, weightsC): 
         #print(w)
        d = {edges[i]: w[i] for i in range(n)}
        #d = {list(graph.edges)[i]: w[i] for i in range(n)}
        nx.set_edge_attributes(graph, d, name="weight")
        #print(d)
        x=algo(graph, readability)
        print(d,x)
        if x:
            with open('results.txt', 'a') as file: 
                file.write(f"Weights:{w}\n")
        i += 1
        if i > 10:
            break
     
          

if __name__=="__main__":
    #feasibleWeights(C6, 3)
    #generateWeightsG(42,3, weightsC)
    feasibleWeights(G,edgesg, 3)