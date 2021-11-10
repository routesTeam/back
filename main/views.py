from django.shortcuts import render

from .forms import CitiesForm
from .models import Route
from .models import *

# Create your views here.
def index(request):
    form = CitiesForm(initial={
      'first_city': request.GET.get('first_city'),
      'second_city': request.GET.get('second_city')
    })
    
    first_city = request.GET.get('first_city')
    second_city = request.GET.get('second_city')

    city = City.objects.all()


    return render(request, "index.html", {
      'form': form,
      'city': city[0].point_x,
      'routes': Route.objects.all().filter(first_city=first_city, second_city=second_city)
    })