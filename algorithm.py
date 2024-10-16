import networkx as nx 
import numpy as np 
import copy
import itertools

B = nx.DiGraph()
B.add_nodes_from([0,2,4], bipartite = 0)
B.add_nodes_from([1,3,5], bipartite = 1)
B.add_weighted_edges_from([(0,1,3), (2,1,2), (0,3, 2), (2,5,2), (4,3,2), (4,5,3)])
nx.set_node_attributes(B, {i : "open" for i in B.nodes}, name="status")
r = 3 #target readability
nx.set_node_attributes(B, {i : np.zeros(r) for i in B.nodes}, name="label")


C = nx.DiGraph()
C.add_nodes_from([0,2], bipartite = 0)
C.add_nodes_from([1,3], bipartite = 1)
C.add_weighted_edges_from([(0,1,2), (0,3, 1), (2,1,1), (2,3,2)])
nx.set_node_attributes(C, {i : np.array([1,2]) for i in C.nodes}, name="label")



#acces the label of node i with B.nodes[i]['label']
#access the weight of an edge e with B.edges[e]['weight]

#this checks if it is a solution: replace by all vertices are closed?
def isSol(B, readability):
    if not isFeasible(B,readability):
        return False 
    else:
        sol = True
        sources = [i for i in B.nodes if B.nodes[i]['bipartite'] == 0]
        targets = [i for i in B.nodes if B.nodes[i]['bipartite'] == 1]
        #sources, targets = nx.bipartite.sets(B)
        for i in sources:
            for j in targets:
                if (i,j) in B.edges:
                    e = (i,j)
                    w = B.edges[e]['weight']
                    if not all(B.nodes[i]['label'][-w:] == B.nodes[j]['label'][:w]):
                        return False 
                    
    return sol 

def isFeasible(B, readability):
    #checks only for undesirede overlaps, but conditions don't have to be satisfied yet
    feasible = True
    sources = [i for i in B.nodes if B.nodes[i]['bipartite'] == 0]
    targets = [i for i in B.nodes if B.nodes[i]['bipartite'] == 1]
    #sources, targets = nx.bipartite.sets(B)
    for i in sources:
        for j in targets:
            if (i,j) in B.edges:
                e = (i,j)
                w = B.edges[e]['weight']
                if undesiredOverlaps(B, i, j, w+1, readability):
                    return False 
            else: 
                if undesiredOverlaps(B, i, j, 1, readability):
                    return False
                #check that there is no overlap
    return feasible 


def undesiredOverlaps(B, u, v, value, readability):
# r is min overlap not allowed 
# u must always be source and v target 
    if B.nodes[u]['bipartite'] != 0 or B.nodes[v]['bipartite'] != 1:
        raise ValueError("Called with Target Source")
    else:
        l1 = B.nodes[u]['label']
        l2 = B.nodes[v]['label']
        overlap = False 
        for i in range(value, readability+1):
            if all(l1[-i:] == l2[:i]) and all(l1[-i:]!= np.zeros(i)) and all(l2[:i] != np.zeros(i)):
                return True 
        return overlap 

def setLabel(B, u, last_used):
    #if node is isolated, set label of length 1
    if B.nodes[u]['bipartite'] == 0:
        lsize = max([1]+[B.edges[(u,v)]['weight'] for v in B.successors(u)])
        for i in range(lsize):
            if B.nodes[u]['label'][-lsize+i] == 0:
                B.nodes[u]['label'][-lsize+i] = last_used +1 
                last_used += 1
    elif B.nodes[u]['bipartite'] == 1:
        lsize = max([1]+[B.edges[(v,u)]['weight'] for v in B.predecessors(u)])
        for i in range(lsize):
            if B.nodes[u]['label'][i] == 0:
                B.nodes[u]['label'][i] = last_used +1 
                last_used += 1
    return last_used 

#queue of vertices, propagate them in order

def isVertexClosed(B, u):
    if B.nodes[u]['bipartite'] == 0:
        for v in B.successors(u):
            w = B.edges[(u,v)]['weight']
            if not all(B.nodes[u]['label'][-w:] == B.nodes[v]['label'][:w]):
                    #print(u,v)
                    return False 
    else: 
        for v in B.predecessors(u): 
            w = B.edges[(v,u)]['weight']
            if not all(B.nodes[v]['label'][-w:] == B.nodes[u]['label'][:w]):
                     return False 
    return True 

#function to propagate to all the neighbors
#be careful to never propagate 0s !!
def propagate(B, u, queue):
    #if it is a source
    lab = B.nodes[u]['label']
    # check only the open successors?
    if B.nodes[u]['bipartite'] == 0:
        
        for v in B.successors(u):
            #if B.nodes[v]['status'] == 'open':
                w = B.edges[(u,v)]['weight']
                old = copy.deepcopy(B.nodes[v]['label'])
                for i in range(w):
                    if lab[-w+i] != 0:
                        B.nodes[v]['label'][i] = lab[-w+i]
                #print(v, B.nodes[v]['label'])
                #B.nodes[v]['label'][:(min(w, len(lab)))] = lab[-(min(w, len(lab))):]
                #print(old)
                if any(B.nodes[v]['label'] != old ):
                    queue.add(v)
        #print("its a source")
    else: 
        for v in B.predecessors(u): 
            #if B.nodes[v]['status'] == 'open':
                w = B.edges[(v,u)]['weight']
                old = copy.deepcopy(B.nodes[v]['label'])
                for i in range(w):
                    if lab[i] != 0:
                        B.nodes[v]['label'][-w+i] = lab[i]
                #B.nodes[v]['label'][-(min(w, len(lab))):] = lab[:(min(w, len(lab)))]
                #print(v, B.nodes[v]['label'])

                if any(B.nodes[v]['label'] != old) :
                    queue.add(v)
                #print(v)
        #print("is target")
    if isVertexClosed(B,u):
        B.nodes[u]['status'] = 'closed'
    return [q for q in queue if B.nodes[q]['status'] == 'open']

def propagateFully(B, u):
    q = propagate(B, u, set())
    while q:
        v = q.pop()
        q = propagate(B, v, q)
        print("queue", q)

#setLabel(B, 5, 0)
#propagateFully(B, 0)




def algo(B, readability):
    last_used= 0 
    nx.set_node_attributes(B, {i : "open" for i in B.nodes}, name="status")
    r = 3 #target readability
    nx.set_node_attributes(B, {i : np.zeros(readability) for i in B.nodes}, name="label")
    open = [v for v in B.nodes] # if B.nodes[v]['status'] == 'open']
    print(open)
    while open: 
        u = open.pop()
        #print(u)
        last_used = setLabel(B, u, last_used)
        #print(B.nodes[u]['label'])
        propagateFully(B, u)
        #[print(i,B.nodes[i]['label']) for i in [0,2,4,1,3,5]]
        open = [v for v in B.nodes if B.nodes[v]['status'] == 'open']
        if not isFeasible(B, readability):
            return False 
        print(open)
    return isSol(B, readability)

    
#filter our symmetries!
def generateWeights(length, readability):
    result = list(itertools.product(range(1, readability + 1), repeat=length))
    
    # If length is 1, return a flat list instead of a list of tuples
    if length == 1:
        return [[x[0]] for x in result]
    return result

graph = nx.DiGraph()
graph.add_nodes_from([0,2], bipartite = 0)
graph.add_nodes_from([1,3], bipartite =1)
graph.add_edges_from([(0,1)]) #, (2,1), (2,3)]) #, (0,3)])

def feasibleWeights(graph, readability):
     n = graph.number_of_edges()
     weights = generateWeights(n, readability)
     print(weights)
     for w in weights: 
         print(w)
         d = {list(graph.edges)[i]: w[i] for i in range(n)}
         nx.set_edge_attributes(graph, d, name="weight")
         print(graph.edges[(0,1)])
         print(d, algo(graph, readability))
         

#feasibleWeights(G, 3)