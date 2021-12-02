import queue
import datetime

def heuristic(vert_a, vert_b):
    return abs(vert_b.point_x - vert_a.point_x) + abs(vert_b.point_y - vert_a.point_y)


def get_min_arrival_time(time_list, time_current):
    time_current_to_date = datetime.datetime.strptime(time_current, '%H:%M')
    for x_time in time_list:
        temp_time = datetime.datetime.strptime(x_time, '%H:%M')
        if (temp_time - time_current_to_date).total_seconds() >= 0:
            return temp_time, x_time
    return datetime.datetime.strptime(time_list[0], '%H:%M'), time_list[0]



def a_star(start_name, goal_name, cities, relations, props_relation, search_feature, departure_time ):

    #just temporary
    schedule = {
        1 : ['10:00', '15:00', '20:00'],
        2 : ['10:00', '15:00', '20:00'],
        3 : ['10:00', '15:00', '20:00'],
        4 : ['10:00', '15:00', '20:00'],
        5 : ['10:00', '15:00', '20:00'],
        6 : ['10:00', '15:00', '20:00'],
        7 : ['10:00', '15:00', '20:00'],
        8 : ['10:00', '15:00', '20:00'],
        9 : ['10:00', '15:00', '20:00'],
        10 : ['10:00', '15:00', '20:00'],
        11 : ['10:00', '15:00', '20:00'],
        12 : ['10:00', '15:00', '20:00'],
        13 : ['10:00', '15:00', '20:00'],
        14 : ['10:00', '15:00', '20:00'],
        15 : ['10:00', '15:00', '20:00'],
        16 : ['10:00', '15:00', '20:00'],
        17 : ['10:00', '15:00', '20:00'],
        18 : ['10:00', '15:00', '20:00']
    }



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

    arrival_departure = {}
    arrival_departure[start_name] = [departure_time, None]


    paths[start_name] = None
    path_exists = False;
    distance[start_name] = 0

    relation_props_in_path = {}
    relation_props_in_path[start_name] = None

    time_waiting = 0
    temp_departure_time = None
    str_time = None


    cities_queue = queue.PriorityQueue()

    cities_queue.put(((0, start_vert.id), start_vert))

    while not cities_queue.empty():
        current_vert = cities_queue.get()[1]

        if current_vert.id in reviewed_verts:
            continue

        temp_arrival_time = arrival_departure[current_vert.name][0]

        if current_vert.name != start_name:
            arrival_departure[paths[current_vert.name]][1] = relation_props_in_path[current_vert.name][3]  # AAAAahahahahahahahahahahahahahahah

        '''print(current_vert.name)
        print(paths[current_vert.name])
        print(relation_props_in_path)
        print(arrival_departure);'''

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
                        dist_to_next = x_prop.time if search_feature else x_prop.cost
                        prop_relation_next = x_prop
                        break

                #calculation waiting time
                (temp_departure_time, str_departure_time)  = get_min_arrival_time(schedule[x_edge.id], temp_arrival_time)

                time_waiting = (temp_departure_time - datetime.datetime.strptime(temp_arrival_time, '%H:%M')).total_seconds() / 60

                if time_waiting < 0:
                    time_waiting = (temp_departure_time +
                                    datetime.timedelta(days=1)
                                    - datetime.datetime.strptime(temp_arrival_time, '%H:%M')).total_seconds() / 60




                next_distance = distance[current_vert.name] + dist_to_next + time_waiting if search_feature else 0 #now with waiting time

                if next_vert.name not in distance or next_distance < distance[next_vert.name]:
                    distance[next_vert.name] = next_distance
                    priority = next_distance + heuristic(goal_vert, next_vert)

                    cities_queue.put(((priority, next_vert.id), next_vert))
                    paths[next_vert.name] = current_vert.name


                    relation_props_in_path[next_vert.name] = [prop_relation_next.relation_type, prop_relation_next.time, prop_relation_next.cost, str_departure_time]

                    print(current_vert.name)
                    print(next_vert.name)
                    print(temp_arrival_time)
                    print(str_departure_time)
                    print(relation_props_in_path)

                    #arrival_departure[current_vert.name][1] = str_departure_time

                    arrival_departure[next_vert.name] = []
                    arrival_departure[next_vert.name].append(datetime.datetime.strftime(
                        temp_departure_time + datetime.timedelta(hours=dist_to_next), '%H:%M'))
                    arrival_departure[next_vert.name].append(None)


        reviewed_verts.append(current_vert.id)


    if not path_exists:
        return "path doesn't exist"

    final_path = []
    final_relation_props_in_path = {}

    temp_city = goal_name
    final_path.append(temp_city)
    while  paths[temp_city] != None:
        temp_city = paths[temp_city]
        final_path.append({'name': temp_city, 'props': relation_props_in_path[temp_city]})
    final_path.reverse()

    final_path[len(final_path)-1] = {'name': final_path[len(final_path)-1], 'props': relation_props_in_path[final_path[len(final_path)-1]]}

    print(final_path)
    print(arrival_departure)


    return final_path





'''
⢀⡴⠑⡄⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠸⡇⠀⠿⡀⠀⠀⠀⣀⡴⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠑⢄⣠⠾⠁⣀⣄⡈⠙⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⢀⡀⠁⠀⠀⠈⠙⠛⠂⠈⣿⣿⣿⣿⣿⠿⡿⢿⣆⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⢀⡾⣁⣀⠀⠴⠂⠙⣗⡀⠀⢻⣿⣿⠭⢤⣴⣦⣤⣹⠀⠀⠀⢀⢴⣶⣆ 
⠀⠀⢀⣾⣿⣿⣿⣷⣮⣽⣾⣿⣥⣴⣿⣿⡿⢂⠔⢚⡿⢿⣿⣦⣴⣾⠁⠸⣼⡿ 
⠀⢀⡞⠁⠙⠻⠿⠟⠉⠀⠛⢹⣿⣿⣿⣿⣿⣌⢤⣼⣿⣾⣿⡟⠉⠀⠀⠀⠀⠀ 
⠀⣾⣷⣶⠇⠀⠀⣤⣄⣀⡀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀ 
⠀⠉⠈⠉⠀⠀⢦⡈⢻⣿⣿⣿⣶⣶⣶⣶⣤⣽⡹⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠉⠲⣽⡻⢿⣿⣿⣿⣿⣿⣿⣷⣜⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣶⣮⣭⣽⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⠿⠿⠿⠛⠉
'''
