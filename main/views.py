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

    city = City.objects.all()

    try:
        res = a_star(first_city, second_city, City.objects.all(), Relation.objects.all(), PropsRelation.objects.all())
    except ValueError as err:
        print(str(err))
        res = None

    return render(request, "index.html", {
      'form': form,
      'city': res,
      'routes': Route.objects.all().filter(first_city=first_city, second_city=second_city)
    })