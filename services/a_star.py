import queue

def heuristic(vert_a, vert_b):
    return abs(vert_b.x - vert_a.x) + abs(vert_b.y - vert_a.y)

def a_start(start_city_name, goal_city_name, vertices, edges, edge_prop):
    for x_vert in vertices:
        if x_vert.city_name == start_city_name:
            start_vert = x_vert
            break

    for x_vert in vertices:
        if x_vert.city_name == goal_city_name:
            goal_vert = x_vert
            break


    our_path = {}
    distance = {}
    our_path[start_city_name] = None
    distance[start_city_name] = 0

    vertices_queue = queue.PriorityQueue()
    vertices_queue.put(start_vert, 0)

    while not our_path.emplty():
        current_vert = vertices_queue.get()

        if current_vert.city_name == goal_vert.city_name:
            break

        for x_edge in edges:
            if x_edge.first_city_id == current_vert and x_edge.second_city_id not in our_path:
                for x_vert in vertices:
                    if x_vert.city_id == x_edge.second_city_id:
                        next_vert = x_vert
                        break

                for x_prop in edge_prop:
                    if x_prop.relation_id == x_edge.relation_id:
                        dist_to_next = x_prop.time
                        break

                next_distance = distance[current_vert.city_name] + dist_to_next

                if next_vert.city_name not in distance or  next_distance < distance[next_vert.city_name]
                    priority = heuristic(goal_vert, next_vert)
                    vertices_queue.put(next_vert, priority)
                    our_path[start_vert] = next_vert.city_id
                    our_path[next_vert.city_name] = current_vert.city_name
