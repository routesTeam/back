from django.http.request import MediaType
from django.http.response import HttpResponse
from django.shortcuts import render
import json
import networkx as nx
import math
import random
import datetime

from .forms import CitiesForm
from .models import Route
from .models import *

from services.a_star import *

# Create your views here.
def index(request):
    form = CitiesForm(initial={
      'first_city': request.GET.get('first_city'),
      'second_city': request.GET.get('second_city')
    })
    
    first_city = request.GET.get('first_city')
    second_city = request.GET.get('second_city')
    priority = request.GET.get('priority')

    city = City.objects.all()
    faster = True if priority == 'fast' else False

    try:
        res = a_star(first_city, second_city, City.objects.all(), Relation.objects.all(), PropsRelation.objects.all(), faster, '11:53')
    except ValueError as err:
        print(str(err))
        res = None

    route = []
    sum = {'time': 0, 'cost': 0}

    if res != None:
        for x in range(len(res)-1):
            sum['time'] += res[x+1]['props'][1]
            sum['cost'] += res[x+1]['props'][2]
            # print(res)
            route.append({'first': {'name': res[x]['name'], 'time': res[x]['time'][1]}, 
                          'props': res[x+1]['props'], 
                          'second': {'name': res[x+1]['name'], 'time': res[x+1]['time'][0]}
                        })
    print("-----------")
    print(route)

    return render(request, "index.html", {
      'form': form,
      'route': route,
      'sum': sum,
      'priority': priority,
      'routes': Route.objects.all().filter(first_city=first_city, second_city=second_city)


    })


def get_schedule(vehicle):

    schedule = []

    time_end = datetime.datetime.strptime('23:59', '%H:%M')

    if vehicle == 'Plane':
        time_deltas = [0.5, 1, 2, 5, 10]
        time_disp = datetime.datetime.strptime('00:00', '%H:%M')
    elif vehicle == 'Train':
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


def getTransports(dist): 
    plane_cost = 4
    plane_speed = 800 

    res = []
    transport = {}
    if dist > 1000:
      transport['name'] = 'самолет'
      transport['price'] = round(plane_cost * dist, 2)
      transport['time'] = round((dist / 800 * 60) + 60, 2)
      res.append(transport)
    
    return res
    # return [['name': 'самолет', 'price': 100, ''],['name': 'самолет', 'price']]


def generator(request):

    G = nx.fast_gnp_random_graph(1000, 0.0115, seed=None, directed=False)

    edge_index = 1
    cities = City.objects.all()
    for x in list(G.edges):
        if x[0] == 0 or x[1] == 0:
            continue
        
        for city in cities:
          if city.id == x[0]:
            first_city_id = city.id
            first_city_lat = city.point_x
            first_city_lng = city.point_y

          if city.id == x[1]:
            second_city_id = city.id
            second_city_lat = city.point_x
            second_city_lng = city.point_y
        
        # relationId = записываем в таблицу relation
        dest = GD(first_city_lat, first_city_lng, second_city_lat, second_city_lng)        
        print(first_city_id, second_city_id)
        print(getTransports(dest))

        edge_index += 1

    return HttpResponse(json.dumps([]), content_type="application/json")
