import math
import random
import datetime


def generate_props_relation(first_city_lat, first_city_lng, second_city_lat, second_city_lng):
    dist = GD(first_city_lat, first_city_lng, second_city_lat, second_city_lng) 
    return get_properties(dist)


def get_schedule(vehicle):

    schedule = []

    time_end = datetime.datetime.strptime('23:59', '%H:%M')

    if vehicle == 'Самолет':
        time_deltas = [0.5, 1, 2, 5, 10]
        time_disp = datetime.datetime.strptime('00:00', '%H:%M')
    elif vehicle == 'Поезд':
        time_deltas = [1, 2, 5, 6, 7, 10]
        time_disp = datetime.datetime.strptime('00:00', '%H:%M')
    else:
        time_deltas = [0.25, 0.5, 1]
        time_disp = datetime.datetime.strptime('08:00', '%H:%M')

    time_disp = time_disp + datetime.timedelta(
        hours=random.choice(time_deltas))

    while time_disp < time_end:
        schedule.append(
            datetime.datetime.strftime(time_disp, '%H:%M'))

        time_disp = time_disp + datetime.timedelta(
            hours=random.choice(time_deltas))
    return schedule




def GD(la1, la2, lo1, lo2):
    # The math module contains the function name "radians" which is used for converting the degrees value into radians.
    lo1 = math.radians(lo1)
    lo2 = math.radians(lo2)
    la1 = math.radians(la1)
    la2 = math.radians(la2)

    # Using the "Haversine formula"
    d_lo = lo2 - lo1
    d_la = la2 - la1
    p = math.sin(d_la / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin(d_lo / 2) ** 2

    q = 2 * math.asin(math.sqrt(p))

    # The radius of earth in kilometres.
    r_km = 6371

    # Then, we will calculate the result
    return q * r_km

def get_prop_object(vehicle_name, dist, cost, speed):
    res = {}
    res['name'] = vehicle_name
    res['price'] = round(cost * dist, 2)
    res['time'] = round((dist / speed * 60) + 60, 2)
    res['shedule'] = get_schedule(res['name'])

    return res

def get_properties(dist): 
    train = False
    bus = False
    plane = False

    plane_cost = 4
    plane_speed = 800 

    train_cost = 2
    train_speed = 70 

    bus_cost = 1
    bus_speed = 100

    auto_speed = 120

    res = []

    if dist > 1000:
      res.append(get_prop_object('Самолет', dist, plane_cost, plane_speed))
      train = random.choices([True, False], weights=(0.95,0.05))
      bus = random.choices([True, False], weights=(0.01,0.99))
      if train:
        res.append(get_prop_object('Поезд', dist, train_cost, train_speed))  
      if bus:
        res.append(get_prop_object('Автобус', dist, bus_cost, bus_speed))
    elif dist > 100:
      res.append(get_prop_object('Поезд', dist, train_cost, train_speed))
      bus = random.choices([True, False], weights=(0.95,0.05))
      if bus:
        res.append(get_prop_object('Автобус', dist, bus_speed, bus_speed))
    else:
      bus = True
      res.append(get_prop_object('Автобус', dist, bus_speed, bus_speed))
      
    if bus:
      res.append({'name': 'авто', 'price': 0, 'time': round((dist / auto_speed * 60) + 60, 2), 'shedule': 'null'})

    return res
    # return [['name': 'самолет', 'price': 100, ''],['name': 'самолет', 'price']]

