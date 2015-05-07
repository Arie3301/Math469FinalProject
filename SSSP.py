__author__ = 'ArieSlobbeT440'


import heapq
import csv
import random

##########
# Hi Andrew!
#
# Please feel free to run the code after you're done looking it over. I have written a little
# 'demonstration' for you, which run some examples and discuss them.
#
# Arie
##########

#helper functions for graph initialization
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
        edge_weight = float(edge_data_line[2])
        make_weighted_link(G, edge_source, edge_target, edge_weight)
    # set unused edges to inf
    #set_edges_to_inf(G)
    return G, vertices_by_name, vertices_by_number
# End of Initialize Airline Graph


# MiniG
def initialize_mini_g():
    G = {}
    edge_set = [('0','1',0),('1','2',8),('1','7',9),('1','15',8),('1','16',7),('2','3',5),('2','5',4),
                ('2','7',6),('3','4',5),('4','6',6),('4','9',3),('5','6',2),('5','8',5),('7','8',5),
                ('7','11',2),('8','9',7),('8','10',2),('8','12',3),('8','13',3),('10','12',4),
                ('11','12',2),('11','17',5),('11','15',9),('12','13',2),('12','14',4), ('14','17',9),
                ('16','17',7)]
    for source, target, weight in edge_set:
        make_weighted_link(G, source, target, weight)
    return G
# End of MiniG

# Dijkstra
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
# End of Dijkstra

# Tuned SWSF
def tuned_swsf(G, reverse_G, distance, parent, updates, directed):
    # initialization
    queue = []
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
        if G[source][target] < weight:  # weight increase
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
            # set labels[current_node] to its consistent value
            labels[target] = float('inf')
            for source2 in reverse_G[target]:  # nodes with edges incoming to target
                if distance[source2] + reverse_G[target][source2] < labels[target]:
                    labels[target] = distance[source2] + reverse_G[target][source2]
        if labels[target] is not distance[target]:
            queue.append(target)
    #main phase
    while len(queue) > 0:
        current_node, current_priority = queue_extract(queue, distance, labels)
        queue.remove(current_node)
        if labels[current_node] <= distance[current_node]:  # current node has found a better path
            # set distance and parent attribute
            distance[current_node] = labels[current_node]
            for potential_parent in reverse_G[current_node]:
                if distance[potential_parent] == labels[potential_parent] and distance[potential_parent] + reverse_G[current_node][potential_parent] == labels[current_node]:
                    parent[current_node] = potential_parent
            # append neighbors to queue that may find shorter distance
            for neighbor in G[current_node]:
                if distance[current_node] + G[current_node][neighbor] < labels[neighbor]:  # neighbor can do better
                    labels[neighbor] = distance[current_node] + G[current_node][neighbor]
                    queue.append(neighbor)
        if labels[current_node] > distance[current_node]:  # current node has not found a better path
            distance_old = distance[current_node]
            distance[current_node] = float('inf')
            # set labels[current_node] to its consistent value
            labels[current_node] = float('inf')
            for source in reverse_G[current_node]:
                if distance[source] + reverse_G[current_node][source] < labels[current_node]:
                    labels[current_node] = distance[source] + reverse_G[current_node][source]
            queue.append(current_node)
            # for edge such that it routed through current_node, recompute best shortest path and insert into heap.
            for neighbor in G[current_node]:
                if distance_old + G[current_node][neighbor] == distance[neighbor] or distance_old + G[current_node][neighbor] == labels[neighbor]:
                    # set labels[neighbor] to its consistent value
                    labels[neighbor] = float('inf')
                    for source3 in reverse_G[neighbor]:
                        if distance[source3] + reverse_G[neighbor][source3] < labels[neighbor]:
                            labels[neighbor] = distance[source3] + reverse_G[neighbor][source3]
                    queue.append(neighbor)

# Helper function for the priority queue of Tuned SWSF
def queue_extract(queue, distance, labels):
    queue = list(set(queue))
    current_node = None
    current_priority = float('inf')
    for node in queue:
        if min(distance[node], labels[node]) < current_priority:
            current_priority = min(distance[node], labels[node])
            current_node = node
    queue.remove(current_node)
    return current_node, current_priority
# end of Tuned SWSF

# First Incremental Dijkstra
def first_incremental_dijkstra(G, reverse_G, distance, parent, updates, directed):
    # initialization
    queue = []
    heapq.heapify(queue)
    for source, target, weight in updates:
        delta = G[source][target] - weight
        if delta < 0:  # Weight increase
            # update G
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
            if parent[target] == source:
                subtree = get_subtree(parent, target)
                for child in subtree:
                    distance[child] -= delta
                for child in subtree:
                    for in_node in reverse_G[child]:
                        if distance[child] > distance[in_node] + reverse_G[child][in_node] and parent[in_node] is not child:
                            new_distance = distance[in_node] + reverse_G[child][in_node]
                            # heap update routine
                            update_heap(queue, new_distance, child, in_node)
        if delta > 0:  # Weight decrease
            # update G
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
            if distance[target] > distance[source] + G[source][target]:
                delta_prime = distance[target] - (distance[source] + G[source][target])
                parent[target] = source
                subtree = get_subtree(parent, target)
                for child in subtree:
                    distance[child] = distance[child] - delta_prime
                for child in subtree:
                    for out_node in G[child]:
                        if distance[out_node] > distance[child] + G[child][out_node]:
                            new_distance = distance[child] + G[child][out_node]
                            new_parent = child
                            # heap update routine
                            update_heap(queue, new_distance, out_node, new_parent)
    # Main Phase
    while len(queue) > 0:
        current_pop = heapq.heappop(queue)
        current_distance = current_pop[0]
        current_node = current_pop[1]
        current_parent = current_pop[2]
        delta = current_distance - distance[current_node]
        if delta < 0:
            parent[current_node] = current_parent
            distance[current_node] = current_distance
            for neighbor in G[current_node]:
                if distance[neighbor] > distance[current_node] + G[current_node][neighbor]:
                    new_distance = distance[current_node] + G[current_node][neighbor]
                    new_parent = current_node
                    update_heap(queue, new_distance, neighbor, new_parent)


# Helper function that returns node v and all its children in the SPT
def get_subtree(parent, v):
    children = [v]
    list1 = [v]
    while len(list1) > 0:
        current_node = list1.pop()
        for node in parent:
            if parent[node] == current_node:
                children.append(node)
                list1.append(node)
    return children


# Helper function for the priority queue of First Incremental Dijkstra
def update_heap(queue, node_priority, node, node_parent):
    old_update = None
    for my_tuple in queue:
        if my_tuple[1] == node:
            old_update = my_tuple
    if old_update is None:
        heapq.heappush(queue, (node_priority, node, node_parent))
        return 0
    else:
        if old_update[0] > node_priority:
            queue.remove(old_update)
            heapq.heapify(queue)
            heapq.heappush(queue, (node_priority, node, node_parent))
            return 0
        else:
            return 0


# Helper function that runs the main function once for updates that increase edge weights, and once for
# updates that decrease edge weights.
def first_inc_dijkstra_batch_init(G, reverse_G, distance, parent, updates, directed):
    increases = []
    decreases = []
    for source, target, weight in updates:
        if G[source][target] > weight:
            decreases.append((source, target, weight))
        else:
            increases.append((source, target, weight))
    first_incremental_dijkstra(G, reverse_G, distance, parent, increases, directed)
    first_incremental_dijkstra(G, reverse_G, distance, parent, decreases, directed)
# End of First Incremental Dijkstra

# Helper functions for data exploration
def dictionary_with_names(distance, vertices_by_number):
    my_dict = {}
    for node_number in distance:
        my_dict[vertices_by_number[node_number]] = distance[node_number]
    return my_dict
# End of Helper functions for data exploration


# Code Demonstration
miniG1 = initialize_mini_g()
reverse_miniG1 = reverse_graph(miniG1)
print("MiniG contains the graph that was used during the presentation to demonstrate the workings of the algorithms.")
print("MiniG:", miniG1)
print("We let '0' be the source node and run Dijkstra to find the parents and distances")
distance1, parent1 = dijkstra(miniG1, '0')
print("Initial distances:", distance1)
print("Initial parents:", parent1)
print("Next, we apply a batch of edge updates and run Tuned SWSF as well as First Incremental Dijkstra.")
print("We will set the weight of edge (15, 11) from 9 down to 2, and the weight of edge (1, 16) from 7 to 17.")

updates = [('15', '11', 2), ('1', '16', 17)]
tuned_swsf(miniG1, reverse_miniG1, distance1, parent1, updates, False)
print("SWSF was run.")
print("New parents:", parent1)
print("New distance:", distance1)

miniG2 = initialize_mini_g()
reverse_miniG2 = reverse_graph(miniG2)
distance2, parent2 = dijkstra(miniG2, '0')
updates = [('15', '11', 2), ('1', '16', 17)]
first_inc_dijkstra_batch_init(miniG2, reverse_miniG2, distance2, parent2, updates, False)
print("Incremental Dijkstra was run.")
print("New parents:", parent2)
print("New distance:", distance2)
print("parents equal: ", parent1 == parent2)
print("distances equal: ", distance1 == distance2)

print("-----------------------------------------------------------------------------------------------------------------------------------------")

print("Next, we test our algorithms on the US Air Lines data set which was retrieved from the Pajek data sets page. Unfortunately, the data set")
print("does not come with any documentation. We know that n = 332 and m = 2126. It was not specified what the weights are supposed to represent.")
print("The weights range from 0.0009 to 0.5326, so it is unlikely that they represent some kind of normalized value. From manual inspection, it")
print("does seem like the weights correspond to physical distance between two airports.")
airlineG, vertices_by_name, vertices_by_number = read_airline_graph('USAir97Vertices.txt', 'USAir97Edges.txt')
reverse_airlineG = reverse_graph(airlineG)
distance1, parent1 = dijkstra(airlineG, '2')
distance_for_printout = dictionary_with_names(distance1, vertices_by_number)
print("We run Dijkstra on the data set with the source node fixed at 'Deadhorse', which is an airfield belonging to a remote outpost on the icy")
print("northern shore of Alaska that goes by the same depressing name (en.wikipedia.org/wiki/Deadhorse,_Alaska). I'd like to visit there sometime.")
print("During summer, of course.")
print("Initial Distances:", distance1)
print("Initial parents:", parent1)
print("The main connection from Deadhorse to the rest of the US is through its connection with Anchorage International Airport. We set the distance")
print("to Anchorage from 0.0866 to 0.0900 and recompute the shortest paths.")
updates = [('2', '8', 0.09)]
tuned_swsf(airlineG, reverse_airlineG, distance1, parent1, updates, False)
print("SWSF was run.")
print("New parents:", parent1)
print("New distance:", distance1)

airlineG2, vertices_by_name2, vertices_by_number2 = read_airline_graph('USAir97Vertices.txt', 'USAir97Edges.txt')
reverse_airlineG2 = reverse_graph(airlineG2)
distance2, parent2 = dijkstra(airlineG2, '2')
updates = [('2', '8', 0.09)]
first_inc_dijkstra_batch_init(airlineG2, reverse_airlineG2, distance2, parent2, updates, False)
print("Incremental Dijkstra was run.")
print("New parents:", parent2)
print("New distance:", distance2)
print("parents equal: ", parent1 == parent2)
print("distances equal: ", distance1 == distance2)

print("------------------------------------------------------------------------------------------------------------------------------------------")
print("When I run the algorithms the distance dictionaries are always the same. This is of course supposed to be the case, since")
print("the algorithms are supposed to find the unique shortest distance to each node. However, the parents dictionaries are NOT equal for Tuned")
print("SWSF and Incremental Dijkstra. What we are seeing is thus that shortest paths are not unique in the airline network, and that our algo-")
print("rithms are finding different shortest-path trees.")
# End of Code Demonstration