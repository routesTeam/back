import queue

def heuristic(vert_a, vert_b):
    return abs(vert_b.point_x - vert_a.point_x) + abs(vert_b.point_y - vert_a.point_y)

def a_star(start_name, goal_name, cities, relations, props_relation):
    for x_vert in cities:
        if x_vert.name == start_name:
            start_vert = x_vert
            break

    for x_vert in cities:
        if x_vert.name == goal_name:
            goal_vert = x_vert
            break


    our_path = {}
    distance = {}
    our_path[start_name] = None
    distance[start_name] = 0

    cities_queue = queue.PriorityQueue()
    cities_queue.put(start_vert, 0)

    while not cities_queue.empty():
        current_vert = cities_queue.get()

        if current_vert.name == goal_vert.name:
            break

        for x_edge in relations:
            if x_edge.first_city_id == current_vert and x_edge.second_city_id not in our_path:
                for x_vert in cities:
                    if x_vert.city_id == x_edge.second_city_id:
                        next_vert = x_vert
                        break

                for x_prop in props_relation:
                    if x_prop.relation_id == x_edge.relation_id:
                        dist_to_next = x_prop.time
                        break

                next_distance = distance[current_vert.name] + dist_to_next

                if next_vert.name not in distance or next_distance < distance[next_vert.name]:
                    distance[next_vert.name] = next_distance
                    priority = next_distance + heuristic(goal_vert, next_vert)
                    cities_queue.put(next_vert, priority)
                    our_path[next_vert.name] = current_vert.name

    return our_path