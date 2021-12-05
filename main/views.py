from django.shortcuts import render

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