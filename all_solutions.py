import networkx as nx
#import matplotlib.pyplot as plt
#import scipy
import itertools
from algorithm import algo
import pickle  # Used to store state as binary data
import os

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
                    x = areWeightsFeasible(nx.induced_subgraph(Graph, subgraph + [vertex]),readability, w)
                    if x:
                        sol.append(w)
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

        with open("solution_filtered.txt", 'w') as file:
            print(f"allowed{sol}")
            file.write(f"allowed for subgraph {subgraph} with len {len(sol)} : {sol}\n")
        #print(f"subgraph append{subgraph}")
        return getSol(Graph, subgraph, sol, readability)
        

if __name__=="__main__":
    #feasibleWeights(C6, 3)
    #generateWeightsG(42,3, weightsC)
    #feasibleWeights(G,edgesg, 3)
    getSol(C, [], [{}], 2)
