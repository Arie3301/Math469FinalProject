__author__ = 'ArieSlobbeT440'


import heapq
import csv

##########
# NOTES
# float('inf') / float('-inf')
# if h is a heap then heapq.function_name(h, [element_name])
##########

#helper functions for graph initialization
def set_edges_to_inf(G):
    for node1 in G:
        for node2 in G:
            if node1 is not node2:
                if node2 not in G[node1]:
                    make_weighted_link(G,node1, node2, float('inf'))

def make_weighted_link(G, node1, node2, weight):
    if node1 not in G:
        G[node1] = {}
    G[node1][node2] = weight
    if node2 not in G:
        G[node2] = {}
    G[node2][node1] = weight

def reverse_graph(G):
    # G must be completely filled for this to work
    reverse_G= {}
    for node1 in G:
        reverse_G[node1] = {}
        for node2 in G[node1]:
            reverse_G[node1][node2] = G[node2][node1]
    return reverse_G
# end of helper functions for graph initialization

# Initialize airline graph
def read_airline_graph(vertex_file, edge_file):
    #read in data structures
    tsv_vertices = csv.reader(open(vertex_file), delimiter=" ", quotechar='"', skipinitialspace=True)
    tsv_edges = csv.reader(open(edge_file), delimiter=" ", quotechar='"', skipinitialspace=True)
    G = {}
    vertices_by_name = {}
    vertices_by_number = {}
    for vertex_data_line in tsv_vertices:
        # access the data stored as a string in a list
        vertex_number = vertex_data_line[0]
        vertex_name = vertex_data_line[1]
        G[vertex_number] = {}
        vertices_by_number[vertex_number] = vertex_name
        vertices_by_name[vertex_name] = vertex_number
    for edge_data_line in tsv_edges:
        edge_source = edge_data_line[0]
        edge_target = edge_data_line[1]
        edge_weight = edge_data_line[2]
        make_weighted_link(G, edge_source, edge_target, edge_weight)
    # set unused edges to inf
    set_edges_to_inf(G)
    return G, vertices_by_name, vertices_by_number

#airlineG, vertices_by_name, vertices_by_number = read_airline_graph('USAir97Vertices.txt', 'USAir97Edges.txt')
#end of initialize airline graph

#miniG
def initialize_mini_g():
    G = {}
    edge_set = [('0','1',1),('1','2',8),('1','7',9),('1','15',8),('1','16',7),('2','3',5),('2','5',4),
                ('2','7',6),('3','4',5),('4','6',6),('4','9',3),('5','6',2),('5','7',5),('7','8',5),
                ('7','11',2),('8','9',7),('8','10',2),('8','12',3),('8','13',3),('10','12',4),
                ('11','12',2),('11','17',5),('11','15',9),('12','13',2),('12','14',4), ('14','17',9),
                ('16','17',7)]
    for source, target, weight in edge_set:
        make_weighted_link(G,source,target,weight)
    return G

miniG = initialize_mini_g()
reverse_miniG = reverse_graph(miniG)
#print(miniG)
#print(reverse_miniG)
# end of miniG

#Dijkstra
def dijkstra(G, s):
    distance = {}
    parent = {}
    for node in G:
        distance[node] = float('inf')
        parent[node] = None
    distance[s] = 0
    queue = []
    heapq.heapify(queue)
    heapq.heappush(queue, (0, s))
    queued_nodes = [s]
    while len(queue) > 0:
        current_node = heapq.heappop(queue)[1]
        queued_nodes.remove(current_node)
        for neighbor in G[current_node]:
            if distance[neighbor] > distance[current_node] + G[current_node][neighbor]:
                #update queue routine
                if neighbor in queued_nodes: #remove neighbor from queue if necessary
                    queue.remove((distance[neighbor], neighbor))
                    heapq.heapify(queue)
                    queued_nodes.remove(neighbor)
                distance[neighbor] = distance[current_node] + G[current_node][neighbor]
                parent[neighbor] = current_node
                heapq.heappush(queue, (distance[neighbor], neighbor))
                queued_nodes.append(neighbor)
    return distance, parent

dis, par = dijkstra(miniG, '0')
#print(dis)
#print(par)
# end of Dijkstra

# Tuned SWSF
def tuned_swsf(G, reverse_G, s, distance, parent, updates):
    # initialization
    queue = []
    queued_nodes = []
    heapq.heapify(queue)
    labels = distance
    for source, target, weight in updates:
        if G[source][target] < weight:  # weight increase
            G[source][target] = weight
            if labels[target] > distance[source] + G[source][target]:
                labels[target] = distance[source] + G[source][target]
        if G[source][target] > weight:  # weight decrease
            G[source][target] = weight
            labels[target] = min(distance[source] + G[source][target], labels[target])
        if labels[target] is not distance[target]:
            priority = min(labels[target], distance[target])
            heapq.heappush(queue, (priority, target, source))
            queued_nodes.append(target)
    #main phase
    while len(queue) > 0:
        current_pop = heapq.heappop(queue)
        current_node = current_pop[1]
        current_parent = current_pop[2]
        queued_nodes.remove(current_node)
        if labels[current_node] < distance[current_node]:
            distance[current_node] = labels[current_node]
            parent[current_node] = current_parent
            for neighbor in G[current_node]:
                if distance[current_node] + G[current_node][neighbor] < labels[neighbor]:
                    labels[neighbor] = distance[current_node] + G[current_node][neighbor]
                    # heap update routine
                    if neighbor in queued_nodes: #remove neighbor from queue if necessary
                        queue.remove((distance[neighbor], neighbor))
                        heapq.heapify(queue)
                        queued_nodes.remove(neighbor)
                    priority = min(labels[neighbor], distance[neighbor])
                    heapq.heappush(queue, (priority, neighbor))
                    queued_nodes.append(neighbor)
        if labels[current_node] > distance[current_node]:
            distance_old = distance[current_node]
            distance[current_node] = float('inf')
            #labels[current_node] =
            # notes to self: Trying set labels[current_node] to con(v) with reverseG. Also wanting to make sure that
            # parent gets carried along properly in the queue and that prospective parents get locked down properly.

# end of Tuned SWSF