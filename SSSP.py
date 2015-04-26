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
    edge_set = [('0','1',0),('1','2',8),('1','7',9),('1','15',8),('1','16',7),('2','3',5),('2','5',4),
                ('2','7',6),('3','4',5),('4','6',6),('4','9',3),('5','6',2),('5','8',5),('7','8',5),
                ('7','11',2),('8','9',7),('8','10',2),('8','12',3),('8','13',3),('10','12',4),
                ('11','12',2),('11','17',5),('11','15',9),('12','13',2),('12','14',4), ('14','17',9),
                ('16','17',7)]
    #edge_set = [('0', '1', 0), ('1', '2', 1), ('1', '5', 6), ('2', '3', 2), ('3', '4', 2), ('4', '5', 2)]
    for source, target, weight in edge_set:
        make_weighted_link(G,source,target,weight)
    return G


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
    # queue contains tuples (priority, node_name, parent_name)
    heapq.heappush(queue, (0, s))
    while len(queue) > 0:
        current_pop = heapq.heappop(queue)
        current_node = current_pop[1]
        for neighbor in G[current_node]:
            if distance[neighbor] > distance[current_node] + G[current_node][neighbor]:
                #update queue routine
                for my_tuple in queue:
                    if my_tuple[1] == neighbor:
                        queue.remove(my_tuple)
                        heapq.heapify(queue)
                distance[neighbor] = distance[current_node] + G[current_node][neighbor]
                parent[neighbor] = current_node
                heapq.heappush(queue, (distance[neighbor], neighbor))
    return distance, parent


# end of Dijkstra

# Tuned SWSF
def tuned_swsf(G, reverse_G, distance, parent, updates, directed):
    # initialization
    queue = []
    heapq.heapify(queue)
    labels = distance.copy()
    for source, target, weight in updates:
        if G[source][target] > weight:  # weight decrease
            G[source][target] = weight
            reverse_G[target][source] = weight
            if not directed:
                G[target][source] = weight
                reverse_G[source][target] = weight
                # set source to be the node closer to s
                if distance[target] < distance[source]:
                    temp = target
                    target = source
                    source = temp
            if labels[target] > distance[source] + G[source][target]:
                labels[target] = distance[source] + G[source][target]
                parent_candidate = source
        if G[source][target] < weight:  # weight increase
            G[source][target] = weight
            reverse_G[target][source] = weight
            if not directed:
                G[target][source] = weight
                reverse_G[source][target] = weight
                # set source to be the node closer to s
                if distance[target] < distance[source]:
                    #temp = target
                    target = source
                    #source = temp
             # set labels[current_node] to its consistent value
            labels[target] = float('inf')
            parent_candidate = None
            for source2 in reverse_G[target]:
                if parent[source2] is not target and labels[source2] + reverse_G[target][source2] < labels[target]:
                    labels[target] = distance[source2] + reverse_G[target][source2]
                    parent_candidate = source2
        if labels[target] is not distance[target]:
            priority = min(labels[target], distance[target])
            heapq.heappush(queue, (priority, target, parent_candidate))
    #main phase
    while len(queue) > 0:
        current_pop = heapq.heappop(queue)
        current_node = current_pop[1]
        current_parent = current_pop[2]
        if labels[current_node] < distance[current_node]:  # current node has found a better path
            distance[current_node] = labels[current_node]
            parent[current_node] = current_parent
            for neighbor in G[current_node]:
                if distance[current_node] + G[current_node][neighbor] < labels[neighbor]:  # neighbor can do better
                    labels[neighbor] = distance[current_node] + G[current_node][neighbor]
                    # heap update routine
                    for my_tuple in queue:
                        if my_tuple[1] == neighbor:
                            queue.remove(my_tuple)
                            heapq.heapify(queue)
                    priority = min(labels[neighbor], distance[neighbor])
                    heapq.heappush(queue, (priority, neighbor, current_node))
        if labels[current_node] > distance[current_node]:  # current node has not found a better path
            distance_old = distance[current_node]
            distance[current_node] = float('inf')
            # set labels[current_node] to its consistent value
            labels[current_node] = float('inf')
            parent_candidate = None
            for source in reverse_G[current_node]:
                if parent[source] is not current_node and labels[source] + reverse_G[current_node][source] < labels[current_node]:
                    labels[current_node] = distance[source] + reverse_G[current_node][source]
                    parent_candidate = source
            # heap update routine
            for my_tuple in queue:
                if my_tuple[1] == current_node:
                    queue.remove(my_tuple)
                    heapq.heapify(queue)
            heapq.heappush(queue, (labels[current_node], current_node, parent_candidate))
            # for edge such that it routed through current_node, recompute best shortest path and insert into heap.
            for neighbor in G[current_node]:
                if distance_old + G[current_node][neighbor] == distance[neighbor]:
                    # set labels[current_node] to its consistent value
                    labels[neighbor] = float('inf')
                    parent_of_neighbor = None
                    for source3 in reverse_G[neighbor]:
                        if labels[source3] + reverse_G[neighbor][source3] < labels[neighbor]:
                            labels[neighbor] = distance[source3] + reverse_G[neighbor][source3]
                            parent_of_neighbor = source3
                    # heap update routine
                    for my_tuple in queue:
                        if my_tuple[1] == neighbor:
                            queue.remove(my_tuple)
                            heapq.heapify(queue)
                            priority = min(labels[neighbor], distance[neighbor])
                    heapq.heappush(queue, (priority, neighbor, parent_of_neighbor))
# end of Tuned SWSF

###testing SWSF
miniG1 = initialize_mini_g()
reverse_miniG1 = reverse_graph(miniG1)
#print(miniG1)
#print(reverse_miniG)

distance1, parent1 = dijkstra(miniG1, '0')
#print(distance1)
#print(parent1)

#updates = [('7', '1', 1)]
#miniG2, distance2, parent2 = tuned_swsf(miniG1, reverse_miniG1, distance1, parent1, updates)

#print(miniG1)
#print(distance1)
#print(parent1)
#tuned_swsf(miniG1, reverse_miniG1, distance1, parent1, updates, False)
#print(parent1)
#print(distance1)
#print(miniG1)

### end of testing SWSF
