from django.http.request import MediaType
from django.http.response import HttpResponse
from django.shortcuts import render
import json
import networkx as nx

from .properties_service import *

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
    hours = request.GET.get('hours')
    minutes = request.GET.get('minutes')

    city = City.objects.all()
    faster = True if priority == 'fast' else False
    is_only_road = True if priority == 'onlyRoad' else False

    time_start = '00:00'
    if hours != None and minutes != None:
      time_start = hours + ':' + minutes
    
    try:
        res = a_star(first_city, second_city, City.objects.all(), Relation.objects.all(), PropsRelation.objects.all(), faster, time_start, only_car=is_only_road)
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
    else:
        print("There is no route")

    print("-----------")
    print(route)

    return render(request, "index.html", {
      'form': form,
      'route': route,
      'sum': sum,
      'priority': priority,
      'selected_hour': hours,
      'selected_minute': minutes,
      'hours': ['0' + str(h) for h in list(range(10))] + [str(h) for h in list(range(10,24))],
      'minutes': ['0' + str(m) for m in list(range(10))] + [str(m) for m in list(range(10,61))],
      'routes': Route.objects.all().filter(first_city=first_city, second_city=second_city)
    })


def testgen(request):
    # city = CityDebug(name='второй город', point_x=0.2341, point_y=1.2345)
    # city.save()
    # relation = RelationDebug(first_city_id=1, second_city_id=2)
    # relation.save()
    # print(relation.id) 
    shedule = 'null'
    props_relation = PropsRelationDebug(relation_type='Авто', time=120, 
                                        cost=0, relation_id=1, schedule=json.dumps(shedule))
    props_relation.save()                                    
    return HttpResponse(json.dumps([]), content_type="application/json")


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
        
        
        relation_from = Relation(first_city_id=first_city_id, second_city_id=second_city_id)
        relation_to = Relation(first_city_id=second_city_id, second_city_id=first_city_id)
        relation_from.save()
        relation_to.save()

        # relationId = записываем в таблицу relation
        relation_from_id = relation_from.id
        relation_to_id = relation_to.id

        props_relation_list = generate_props_relation(first_city_lat, first_city_lng, second_city_lat, second_city_lng)

        for prop in props_relation_list:
          props_relation_from = PropsRelation(relation_type=prop['name'], time=prop['time'], 
                                        cost=prop['price'], 
                                        relation_id=relation_from_id, 
                                        schedule=json.dumps(prop['shedule']))
          props_relation_to = PropsRelation(relation_type=prop['name'], time=prop['time'], 
                                        cost=prop['price'], 
                                        relation_id=relation_to_id, 
                                        schedule=json.dumps(prop['shedule']))                              
          props_relation_from.save()  
          props_relation_to.save()
        
        edge_index += 1

    return HttpResponse(json.dumps([]), content_type="application/json")
