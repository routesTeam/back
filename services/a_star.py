import json
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



def a_star(start_name, goal_name, cities, relations, props_relation, search_feature, departure_time, only_car ):



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

    #store our super ultra cool the shortest path
    paths[start_name] = None
    path_exists = False;
    distance[start_name] = 0

    #store propeties of relation in our path
    relation_props_in_path = {}
    relation_props_in_path[start_name] = None

    time_waiting = 0
    temp_departure_time = None


    cities_queue = queue.PriorityQueue()

    cities_queue.put(((0, start_vert.id), start_vert))

    while not cities_queue.empty():
        #get vert from queueueueueueueueueueueu
        current_vert = cities_queue.get()[1]

        #we won't review verst that we visited
        if current_vert.id in reviewed_verts:
            continue

        #time of arrival in current city
        temp_arrival_time = arrival_departure[current_vert.name][0]

        #save departure time from <relation_props_in_path> from previous city according to schedule

        if current_vert.name != start_name:
            arrival_departure[paths[current_vert.name]][1] = relation_props_in_path[current_vert.name][3]  # AAAAahahahahahahahahahahahahahahah
        #paths --------> previous city
        #current relation_props_in_path ----------> saves departure time from previous city
        #we came from paths[current_vert.name] |||||| algorithm works this way


        if current_vert.name == goal_vert.name:
            path_exists = True
            break

        for x_edge in relations:
            if x_edge.first_city_id == current_vert.id and x_edge.second_city_id not in reviewed_verts:

                for x_vert in cities:
                    if x_vert.id == x_edge.second_city_id:
                        next_vert = x_vert
                        break

                #get property of relation
                for x_prop in props_relation:
                    if x_prop.relation_id == x_edge.id:
                        dist_to_next = x_prop.time if search_feature else x_prop.cost
                        prop_relation_next = x_prop


                        if only_car and prop_relation_next.relation_type != 'авто':
                            continue

                        if not only_car and prop_relation_next.relation_type == 'авто':
                            continue
                        #calculation waiting time


                        #get earlier time in object and string

                        schedule = [x.replace('"','') for x in prop_relation_next.schedule[1:-1].split(', ')]

                        if not only_car:
                            (temp_departure_time, str_departure_time) = get_min_arrival_time(schedule, temp_arrival_time)

                            #we are waiting vehicle - waiting time calculation
                            time_waiting = (temp_departure_time - datetime.datetime.strptime(temp_arrival_time, '%H:%M')).total_seconds() / 3600

                            #if time is negative (when vehicle does not run and we need to wait until tomorrow)
                            if time_waiting < 0:
                                time_waiting = (temp_departure_time +
                                                datetime.timedelta(days=1)
                                                - datetime.datetime.strptime(temp_arrival_time, '%H:%M')).total_seconds() / 3600
                        else:
                            temp_departure_time = datetime.datetime.strptime(temp_arrival_time, '%H:%M') + datetime.timedelta(hours=1)
                            str_departure_time = datetime.datetime.strftime( temp_departure_time, '%H:%M')




                        next_distance = distance[current_vert.name] + dist_to_next + (time_waiting if (search_feature and not only_car) else 0) #now with waiting time
                        #next_distance = distance[current_vert.name] + dist_to_next

                        if next_vert.name not in distance or next_distance < distance[next_vert.name]:

                            distance[next_vert.name] = next_distance
                            priority = next_distance + heuristic(goal_vert, next_vert)

                            #put vert in queue - (priority + next_vert.id) is real prioruty in queue
                            cities_queue.put(((priority, next_vert.id), next_vert))


                            paths[next_vert.name] = current_vert.name

                            relation_props_in_path[next_vert.name] = [prop_relation_next.relation_type, prop_relation_next.time, prop_relation_next.cost, str_departure_time]
                                                                                                                                                           #add departure_time


                            #add time of arrival to next vertex
                            arrival_departure[next_vert.name] = [] #allocare list
                            arrival_departure[next_vert.name].append(datetime.datetime.strftime(
                                temp_departure_time + datetime.timedelta(hours=dist_to_next), '%H:%M'))
                            arrival_departure[next_vert.name].append(None)


        reviewed_verts.append(current_vert.id)


    if not path_exists:
        return None

    final_path = []
    final_relation_props_in_path = {}

    temp_city = goal_name
    while  paths[temp_city] != None:
        temp_city = paths[temp_city]
        if relation_props_in_path[temp_city] != None:
          relation_props_in_path[temp_city][1] = round(relation_props_in_path[temp_city][1] / 60, 1)
        final_path.append({'name': temp_city, 'props': relation_props_in_path[temp_city], 'time': arrival_departure[temp_city]})
        
        
    final_path.reverse()

    if relation_props_in_path[goal_name] != None:
      relation_props_in_path[goal_name][1] = round(relation_props_in_path[goal_name][1] / 60, 1)

    final_path.append({'name': goal_name, 'props': relation_props_in_path[goal_name], 'time': arrival_departure[goal_name]})

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
