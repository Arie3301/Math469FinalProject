__author__ = 'ArieSlobbeT440'


import heapq
import csv

##########
# NOTES
# float('inf') / float('-inf')
# if h is a heap then heapq.function_name(h, [element_name])
##########

#helper function for graph initialization
def set_edges_to_inf(G):
    for node1 in G:
        for node2 in G:
            if node1 is not node2:
                if node2 not in G[node1]:
                    make_weighted_link(G,node1, node2, float('inf'))
# end of helper functior for graph initialization

# Initialize airline graph
def make_weighted_link(G, node1, node2, weight):
    if node1 not in G:
        G[node1] = {}
    G[node1][node2] = weight
    if node2 not in G:
        G[node2] = {}
    G[node2][node1] = weight


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
print(miniG)
# end of miniG

#Dijkstra
def dijkstra(G, v):
    dist_so_far = []
    dist_so_far[v] = 0
    final_dist = {}
    while len(final_dist) < len(G):
        w = shortest_dist_node(dist_so_far)
        # lock it down!
        final_dist[w] = dist_so_far[w]
        del dist_so_far[w]
        for x in G[w]:
            if x not in final_dist:
                if x not in dist_so_far:
                    dist_so_far[x] = final_dist[w] + G[w][x]
                elif final_dist[w] + G[w][x] < dist_so_far[x]:
                    dist_so_far[x] = final_dist[w] + G[w][x]
    return final_dist

def dijkstra2(G, s):
    distance = {}
    parent = {}
    for node in G:
        distance[node] = float('inf')
        parent[node] = None
    queue = []
    heapq.heapify(queue)
    heapq.heappush(queue, (0, s))
    queued_nodes = [s]
    while len(queue) > 0:
        current_node = heapq.heappop(queue)
        queued_nodes.remove(current_node)
        for neighbor in G[current_node]:
            if distance[neighbor] > distance[current_node] + G[current_node][neighbor]:
                distance[neighbor] = distance[current_node] + G[current_node][neighbor]
                parent[neighbor] = current_node
                #
                if neighbor in queued_nodes:
                    #remove from queue
                #update queue with neighbor properly
                #
    return distance, parent

dis, par = dijkstra2(miniG, '0')
print(dis)
print(par)
# end of Dijkstra