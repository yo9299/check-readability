import gadgets 
import itertools
from algorithm import algo
import networkx as nx 

G = nx.DiGraph()

source_nodes = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28]
target_nodes = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29]

G.add_nodes_from(source_nodes, bipartite=0)  
G.add_nodes_from(target_nodes, bipartite=1)  

edgesg =[(0,1), (2,1), (2,3), (4, 3), (4,5), (0, 5), (0,7) , (6, 1), (6,7), (8,7),(6,9), (8,9), ( 10, 1), (2,11), (10, 11), (10,13), (12, 11), (12,13), (2,15), (14,3), (14,15), (16, 15), (14, 17), (16, 17), (18, 3), (4, 19), (18,19), (18, 21), (20, 19), (20,21), (4, 23), (22, 5), (22,23), (24,23), (22,25), (24,25), (26, 5), (0,27), (26,27), (26, 29), (28, 27), (28,29)]

G.add_edges_from(edgesg)

def generateWeights(allowed, readability, newEdges):
    # allowed is a dictionary of pairs edges, weights
    #new edges is a list of edges not in allowed
   
    for remaining in itertools.product(range(1, readability + 1), repeat=len(newEdges)):
        # Combine the dictionary's allowed value with the remaining sequence
        yield allowed | {edge: remaining[i] for i, edge in enumerate(newEdges)}



def getEdges(Graph, subgraph, vertex):
    #subgraph is a list of vertices in graph, vertex a vertex not in subgraph, returns list of edges from vertex to subgraph
    if Graph.nodes[vertex]['bipartite']==0 and Graph.successors(vertex):
        return [( vertex, x) for x in Graph.successors(vertex) if x in subgraph]
    elif Graph.predecessors(vertex): 
        return [(x, vertex) for x in Graph.predecessors(vertex) if x in subgraph]
    else: 
        return [] 
    

def areWeightsFeasible(graph, readability, weights):
    #weights is a dictionary, returns boolean
    n = graph.number_of_edges()
    nx.set_edge_attributes(graph, weights, name="weight")
    #print(d)
    x=algo(graph, readability)
    #print(x)
    return x 

def generateWeightsSubgraph(Graph, subgraph, allowed, readability, vertex):
    #allowed is a list of dict, subgraph a list of vertices
    newEdges = getEdges(Graph, subgraph, vertex)
    sol = [] 
    for a in allowed:
        for w in generateWeights(a, readability, newEdges):
            #check if feasible and append to results
            #have to call with subgraph not graph
            x = areWeightsFeasible(nx.induced_subgraph(Graph, subgraph + [vertex]),readability, w)
            #print(x)
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
    #at each step, pick a vertex in the connected component, allowed=generateWeights. When no more 
    #vertices left, return allowed.
    #allowed is a list of dict 
    if pickVertex(Graph, subgraph)==None:
        return allowed 
    else:
        v = pickVertex(Graph, subgraph)
        sol = generateWeightsSubgraph(Graph,subgraph, allowed, readability, v)
        subgraph.append(v)

        with open("solution.txt", 'a') as file:
            print(f"allowed{sol}")
            file.write(f"allowed for subgraph {subgraph} : {sol}\n")
        #print(f"subgraph append{subgraph}")
        return getSol(Graph, subgraph, sol, readability)
        
C = nx.DiGraph()
C.add_nodes_from([0,2], bipartite = 0)
C.add_nodes_from([1,3], bipartite = 1)
C.add_edges_from([(0,1), (0,3), (2,1), (2,3)])
#generateWeightsSubgraph(Graph, [0,1,2,3,4], {(0, 1): 1, (2, 1): 2, (2, 3): 1, (4, 3): 2}, 3, 5)

allowed = {(0, 1): 1, (2, 1): 2, (2, 3): 1, (4, 3): 2, (4, 5): 1, (0, 5): 2}

test = {(0, 1): 1, (2, 1): 2, (2, 3): 1, (4, 3): 2, (4, 5): 1, (0, 5): 2, (0, 7): 1, (0, 27): 3, (6, 1): 1, (6, 7): 1, (10, 1): 3}

#ind = nx.induced_subgraph(G, [0,1,2,3,4,5,6,7,10, 27 ])

if __name__=="__main__":
    getSol(G, [0,1,2,3,4,5], [allowed], 3)
