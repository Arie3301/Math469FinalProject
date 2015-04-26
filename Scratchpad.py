__author__ = 'ArieSlobbeT440'

listt = [('a','b','c'),('d','e','f')]

# for item1 in listt:
#     print

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
    heapq.heappush(queue, (0, s, None))
    queued_nodes = {s: None}
    while len(queue) > 0:
        current_pop = heapq.heappop(queue)
        current_node = current_pop[1]
        current_parent = current_pop[2]
        del queued_nodes[current_node]
        for neighbor in G[current_node]:
            if distance[neighbor] > distance[current_node] + G[current_node][neighbor]:
                #update queue routine
                if neighbor in queued_nodes: #remove neighbor from queue if necessary
                    queue.remove((distance[neighbor], neighbor, queued_nodes[neighbor]))
                    heapq.heapify(queue)
                    del queued_nodes[neighbor]
                distance[neighbor] = distance[current_node] + G[current_node][neighbor]
                parent[neighbor] = current_node
                heapq.heappush(queue, (distance[neighbor], neighbor, current_node))
                queued_nodes[neighbor] = current_node
    return distance, parent

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
            if labels[target] > distance[source] + G[source][target]:
                labels[target] = distance[source] + G[source][target]
                parent_candidate = source
        if G[source][target] < weight:  # weight increase
            G[source][target] = weight
            reverse_G[target][source] = weight
            if not directed:
                G[target][source] = weight
                reverse_G[source][target] = weight
            labels[target] = min(distance[source] + G[source][target], labels[target])
             # set labels[current_node] to its consistent value
            if labels[target] != 0:
                labels[target] = float('inf')
                parent_candidate = None
                for source2 in reverse_G[target]:
                    if labels[source2] + reverse_G[target][source2] < labels[target]:
                        labels[target] = labels[source2] + reverse_G[target][source2]
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
                if labels[source] + reverse_G[current_node][source] < labels[current_node]:
                    labels[current_node] = labels[source] + reverse_G[current_node][source]
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
                            labels[neighbor] = labels[source3] + reverse_G[neighbor][source3]
                            parent_of_neighbor = source3
                    # heap update routine
                    for my_tuple in queue:
                        if my_tuple[1] == neighbor:
                            queue.remove(my_tuple)
                            heapq.heapify(queue)
                            priority = min(labels[neighbor], distance[neighbor])
                    heapq.heappush(queue, (priority, neighbor, parent_of_neighbor))
    #return G, distance, parent
# end of Tuned SWSF
