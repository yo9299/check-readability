import networkx as nx
#import matplotlib.pyplot as plt
#import scipy
import itertools
from algorithm import algo
import pickle  # Used to store state as binary data
import os 
from all_solutions import pickVertex, generateWeightsSubgraph

C = nx.DiGraph()
C.add_nodes_from([0,2], bipartite = 0)
C.add_nodes_from([1,3], bipartite = 1)
C.add_edges_from([(0,1), (0,3), (2,1), (2,3)])
e = [(0,1), (0,3), (2,1), (2,3)]

G = nx.DiGraph()
source_nodes = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28]
target_nodes = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29]

d = {(0, 1): 1, (2, 1): 2, (2, 3): 1, (4, 3): 2, (4, 5): 1, (0, 5): 2, (0, 7): 1, (6, 1): 1, (6, 7): 1, (8, 7): 1, (6, 9): 1, (8, 9): 1, (10, 1): 1, (2, 11): 1, (10, 11): 1, (10, 13): 1, (12, 11): 1, (12, 13): 1, (2, 15): 1, (14, 3): 1, (14, 15): 1, (16, 15): 1, (14, 17): 1, (16, 17): 1, (18, 3): 1, (4, 19): 1, (18, 19): 1, (18, 21): 2, (20, 19): 3, (20, 21): 2, (4, 23): 3, (22, 5): 3, (22, 23): 1, (24, 23): 1, (22, 25): 1, (24, 25): 1, (26, 5): 1, (0, 27): 3, (26, 27): 3, (26, 29): 2, (28, 27): 2, (28, 29): 1} 

d1= {(0, 1): 1, (2, 1): 2, (2, 3): 1, (4, 3): 2, (4, 5): 1, (0, 5): 2}

G.add_nodes_from(source_nodes, bipartite=0)  
G.add_nodes_from(target_nodes, bipartite=1)  

edgesg =[(0,1), (2,1), (2,3), (4, 3), (4,5), (0, 5), (0,7) , (6, 1), (6,7), (8,7),(6,9), (8,9), ( 10, 1), (2,11), (10, 11), (10,13), (12, 11), (12,13), (2,15), (14,3), (14,15), (16, 15), (14, 17), (16, 17), (18, 3), (4, 19), (18,19), (18, 21), (20, 19), (20,21), (4, 23), (22, 5), (22,23), (24,23), (22,25), (24,25), (26, 5), (0,27), (26,27), (26, 29), (28, 27), (28,29)]

newe=[(0,1), (2,1), (2,3), (4, 3), (4,5), (0, 5), (0,7) , (6, 1), (6,7), ( 10, 1), (2,11), (10, 11), (2,15), (14,3), (14,15), (18, 3), (4, 19), (18,19), (4, 23), (22, 5), (22,23), (26, 5), (0,27), (26,27)]
G.add_edges_from(edgesg)

weightsC = [(1,2,1,2,1,2)]#, 1,1,1,3,3,2, 3,3,1,1,1,1, 1,1,1,3,3,2, 3,3,1,1,1,1, 1,1,1,3,3,2, 3,3,1,1,1)] #[(1, 1, 2, 1, 1, 3),(1, 1, 2, 3, 1, 2),(1, 1, 2, 3, 1, 3),(1, 1, 3, 1, 1, 3),(1, 1, 3, 1, 2, 3),(1, 1, 3, 2, 1, 3),(1, 2, 1, 2, 1, 3),(1, 2, 1, 3, 1, 3),(1, 2, 2, 3, 1, 3),(1, 3, 2, 1, 3, 2)]

weightsG = (1,2,1,2,1,2, 1,1,1,2,2,3, 3,3,1,1,1,1, 1,1,1,2,2,3, 3,3,1,1,1,1, 1,1,1,2,2,3, 3,3,1,1,1,2)
counter  = (1,3,1,2,1,2, 1,1,1,2,2,3, 2,2,1,3,3,1, 1,1,1,2,2,3, 3,3,1,1,1,1, 1,1,1,2,2,3, 3,3,1,1,1,2)

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

def dictToTuple(d1, d2):
    c1, c2, r1,r2 = [],[],[],[]
    for e in [(0,1), (2,1), (2,3), (4, 3), (4,5), (0, 5)]:
        c1.append(d1[e])
        c2.append(d2[e])
    for e in [(0,7) , (6, 1), (6,7), ( 10, 1), (2,11), (10, 11), (2,15), (14,3), (14,15), (18, 3), (4, 19), (18,19), (4, 23), (22, 5), (22,23), (26, 5), (0,27), (26,27)]:
        r1.append(d1[e])
        r2.append(d2[e])
    return c1,c2,r1, r2

def equivalentNewGadgets(w1, w2):
    """ checks whether two weight tuples are equivalent for the gadget (ie rotations of the gadget)"""
    c1 ,c2, r1,r2 = dictToTuple(w1,w2)
    for i in range(5):
        sol = True 
        if not isRotation(c1, c2, [i]) or not isRotation(r1, r2, [3*i]):
            sol = False 
        if sol:
            return True
    return False

def equivalentGadgets(w1, w2):
    """ checks whether two weight tuples are equivalent for the gadget (ie rotations of the gadget)"""
    c1 = w1[:6]
    r1 = w1[-len(w1) +6 :]
    c2 = w2[:6]
    r2 = w2[-len(w1) +6 :]
    for i in range(5):
        sol = True 
        if not isRotation(c1, c2, [i]) or not isRotation(r1, r2, [6*i]):
            sol = False 
        if sol:
            return True
    return False 

def generateWeightsG(length, readability, allowed_tuples):
    """ Given a set of allowed tuples, completes them to length length with ints from 1 to readability
    yields a generator for memory efficiency, but doesn't eliminate duplicates (rotatios, etc.)
    However, if calles with allowed_tuples = dict with weights of the cycle, no duplicates should arise.
    """
    allowed_set = set(allowed_tuples)  
    for allowed in allowed_set:
        for remaining in itertools.product(range(1, readability + 1), repeat=length-6):#length - 6):
            yield allowed + remaining



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


def getSol(Graph, subgraph, allowed, readability):
    """
    Graph: networkx bipartite digraph
    subgraph: list of vertices for which we have a solution of the subgraph induced by them
    allowed: list of partial dictionaries of edge weights, contains all the sets of weights feasible by the subgraph induced by vertices in list --subgraph
    readability: target value of readability.
    """
    if pickVertex(Graph, subgraph)==None:
        return allowed 
    else:
        v = pickVertex(Graph, subgraph)
        sol = generateWeightsSubgraph(Graph,subgraph, allowed, readability, v)
        subgraph.append(v)

        with open("results.txt", 'w') as file:
            print(f"allowed {sol}")
            file.write(f"allowed for subgraph {subgraph} with len {len(sol)} : {sol}\n")
        #print(f"subgraph append{subgraph}")
        return getSol(Graph, subgraph, sol, readability)
    
        


if __name__=="__main__":
    #feasibleWeights(C6, 3)
    #generateWeightsG(42,3, weightsC)
    #feasibleWeights(G,edgesg, 3)
    """ 
    call getSol

    graph: networkx bipartite digraph
    subgraph: list of vertices which appear in the allowed dict
    allowed: list of dictionaries containing all the weights of edges in the graph induced by subgraph
    readability: target readability 
    
    """
    getSol(G, [0,1,2,3,4,5], [d1], 3)
    print("hola")