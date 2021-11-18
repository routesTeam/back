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
        res = a_star(first_city, second_city, City.objects.all(), Relation.objects.all(), PropsRelation.objects.all(), faster)
    except ValueError as err:
        print(str(err))
        res = None

    return render(request, "index.html", {
      'form': form,
      'city': res,
      'priority': priority,
      'routes': Route.objects.all().filter(first_city=first_city, second_city=second_city)
    })