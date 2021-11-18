import queue

def heuristic(vert_a, vert_b):
    return abs(vert_b.point_x - vert_a.point_x) + abs(vert_b.point_y - vert_a.point_y)

def a_star(start_name, goal_name, cities, relations, props_relation):

    start_vert = None
    goal_vert = None

    for x_vert in cities:
        if x_vert.name == start_name:
            start_vert = x_vert
            break

    for x_vert in cities:
        if x_vert.name == goal_name:
            goal_vert = x_vert
            break

    if start_vert is None:
        raise ValueError("There is no such city: " + str(start_name))

    if goal_vert is None:
        raise ValueError("There is no such city: " + str(goal_name))

    paths = {}
    distance = {}
    reviewed_verts = []

    paths[start_name] = None
    path_exists = False;
    distance[start_name] = 0


    cities_queue = queue.PriorityQueue()

    cities_queue.put(((0, start_vert.id), start_vert))

    while not cities_queue.empty():
        current_vert = cities_queue.get()[1]
        if current_vert.name == goal_vert.name:
            path_exists = True
            break

        for x_edge in relations:
            if x_edge.first_city_id == current_vert.id and x_edge.second_city_id not in reviewed_verts:
                for x_vert in cities:
                    if x_vert.id == x_edge.second_city_id:
                        next_vert = x_vert
                        break

                for x_prop in props_relation:
                    if x_prop.relation_id == x_edge.id:
                        dist_to_next = x_prop.time
                        break

                next_distance = distance[current_vert.name] + dist_to_next

                if next_vert.name not in distance or next_distance < distance[next_vert.name]:
                    distance[next_vert.name] = next_distance
                    priority = next_distance + heuristic(goal_vert, next_vert)

                    cities_queue.put(((priority, next_vert.id), next_vert))
                    print(str(next_vert.id) + ' ' + str(priority))
                    paths[next_vert.name] = current_vert.name
        print(distance)
        reviewed_verts.append(current_vert.id)
        print(reviewed_verts)


    if not path_exists:
        return "path doesn't exist"

    final_path = []

    temp_city = goal_name
    final_path.append(temp_city)
    while  paths[temp_city] != None:
        temp_city = paths[temp_city]
        final_path.append(temp_city)
    final_path.reverse()
    return distance