import networkx as nx
#import matplotlib.pyplot as plt
#import scipy
import itertools
from algorithm import algo
import pickle  # Used to store state as binary data
import os
from gadgets import equivalentNewGadgets

C = nx.DiGraph()
C.add_nodes_from([0,2], bipartite = 0)
C.add_nodes_from([1,3], bipartite = 1)
C.add_edges_from([(0,1), (0,3), (2,1), (2,3)])

def generateWeights(allowed, readability, newEdges):
    # allowed is a dictionary of pairs edges, weights
    #new edges is a list of edges not in allowed
   
    for remaining in itertools.product(range(1, readability + 1), repeat=len(newEdges)):
        yield allowed | {edge: remaining[i] for i, edge in enumerate(newEdges)}


def areWeightsFeasible(graph, readability, weights):
    #weights is a dictionary, returns boolean
    n = graph.number_of_edges()
    nx.set_edge_attributes(graph, weights, name="weight")
    x=algo(graph, readability)
    return x 

def getEdges(Graph, subgraph, vertex):
    #subgraph is a list of vertices in graph, vertex a vertex not in subgraph, returns list of edges from vertex to subgraph
    if Graph.nodes[vertex]['bipartite']==0 and Graph.successors(vertex):
        return [( vertex, x) for x in Graph.successors(vertex) if x in subgraph]
    elif Graph.predecessors(vertex): 
        return [(x, vertex) for x in Graph.predecessors(vertex) if x in subgraph]
    else: 
        return [] 
 
def generateWeightsSubgraph(Graph, subgraph, allowed, readability, vertex):
    #allowed is a list of dict, subgraph a list of vertices
    newEdges = getEdges(Graph, subgraph, vertex)
    sol = [] 
    for a in allowed:
        for w in generateWeights(a, readability, newEdges):
            #check if feasible and append to results
            #have to call with subgraph not graph
            if subgraph + [vertex] == list(Graph.nodes):
                repeated = False 
                for v in sol:
                    
                    if equivalentNewGadgets(v, w):    
                        repeated = True 
                        break
                if not repeated:
                    x = areWeightsFeasible(nx.induced_subgraph(Graph, subgraph + [vertex]),readability, w)
                    if x:
                        sol.append(w)
                    if not (w[(0,1)] == 1 and w[(2,1)]==1 and w[(4,5)] == 1):
                        with open("dif_new_gadget.txt", 'w') as file:
                            file.write(f"allowed for subgraph {subgraph} : {w}\n")

            else:
                x = areWeightsFeasible(nx.induced_subgraph(Graph, subgraph + [vertex]),readability, w)
                if x :
                    sol.append(w)
    return sol 

def pickVertex(Graph, subgraph):
    #subgraph is list of vertices
    if not subgraph:
        return list(Graph.nodes)[0]
    else:
        for v in subgraph:
            for u in list(Graph.successors(v))+list(Graph.predecessors(v)):
                if u not in subgraph:
                    return u 
    return None 
    #given a connected graph, it will always return a vertex, none only if subgraph=G 

def getSol(Graph, subgraph, allowed, readability):
    """
    Graph: networkx bipartite digraph
    subgraph: list of vertices for which we have a solution of the subgraph induced by them
    allowed: list of partial dictionarys of edge weights, contains all the sets of weights feasible by the subgraph induced by vertices in list --subgraph
    readability: target value of readability.
    """
    if pickVertex(Graph, subgraph)==None:
        return allowed 
    else:
        v = pickVertex(Graph, subgraph)
        sol = generateWeightsSubgraph(Graph,subgraph, allowed, readability, v)
        subgraph.append(v)
            #check if it is the rotation of existing
        with open("solution_new_gadget.txt", 'w') as file:
            print(f"allowed{sol}")
            file.write(f"allowed for subgraph {subgraph} with len {len(sol)} : {sol}\n")
        #print(f"subgraph append{subgraph}")
        return getSol(Graph, subgraph, sol, readability)
        
def main(graph, readability):
    """ 
    returns all feasible solutions for a given graph
    graph:networkx bipartite digraph
    readability: integer
    creates file with sols
    """
    getSol(graph, [], [{}], readability)


G = nx.DiGraph()
source_nodes = [0, 2, 4, 6, 10, 14, 18, 22, 26]
target_nodes = [1, 3, 5, 7, 11, 15, 19, 23, 27]

G.add_nodes_from(source_nodes, bipartite=0)  
G.add_nodes_from(target_nodes, bipartite=1)  

newe=[(0,1), (2,1), (2,3), (4, 3), (4,5), (0, 5), (0,7) , (6, 1), (6,7), ( 10, 1), (2,11), (10, 11), (2,15), (14,3), (14,15), (18, 3), (4, 19), (18,19), (4, 23), (22, 5), (22,23), (26, 5), (0,27), (26,27)]

G.add_edges_from(newe)

if __name__=="__main__":
    #feasibleWeights(C6, 3)
    #generateWeightsG(42,3, weightsC)
    #feasibleWeights(G,edgesg, 3)
    main(G, 3)
    print(0)


