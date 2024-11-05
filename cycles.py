import itertools
import networkx as nx 
from algorithm import algo 

C4 = nx.DiGraph()
C4.add_nodes_from([0,2], bipartite = 0)
C4.add_nodes_from([1,3], bipartite = 1)
C4.add_edges_from([(0,1), (0,3), (2,1), (2,3)])
e4 = [(0,1), (0,3), (2,1), (2,3)]

C6 = nx.DiGraph() 
C6.add_nodes_from([0,2,4], bipartite=0)  # Set of sources
C6.add_nodes_from([1,3,5], bipartite=1)  # Set of targets
C6.add_edges_from([(0,1), (2,1), (2,3), (4, 3), (4,5), (0, 5)])
e6 = [(0,1), (2,1), (2,3), (4, 3), (4,5), (0, 5)]



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

def areWeightsFeasible(graph, edges, readability, weights):
    """ 
    creates a weighted graph
    """
    n = graph.number_of_edges()
    d = {edges[i]: weights[i] for i in range(n)}
    #d = weights
    nx.set_edge_attributes(graph, d, name="weight")
    #print(d)
    x=algo(graph, readability)
    print(d,x)
    return x 

def feasibleWeightsC(graph, edges, readability):
    n = graph.number_of_edges()
     #weights = generateWeightsG(n, readability, weightsC)
     #print(weights)
    i = 0
    for w in generateWeightsCycle(n, readability): 
        x = areWeightsFeasible(graph, edges, readability, w)
        if x:
            with open('results.txt', 'a') as file: 
                file.write(f"Weights:{w}\n")
            print(w)
        i += 1


def generateWeightsCycle(length, readability):
    result = []
    seen = set()  
    for combination in itertools.product(range(1, readability + 1), repeat=length):
        if not any(isRotation(combination, existing, list(range(1, length))) for existing in seen):
            result.append(combination)  
            seen.add(combination)  
    return result


def main(graph, edges, readability):
    """ 
    computes all the tuples of feasible weights and writes them in file results.txt
    Call with C4, e4 3 for cycle of length 4
    C6, e6, 3
    """
    feasibleWeightsC(graph, edges, readability)