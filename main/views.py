from django.shortcuts import render

from .forms import CitiesForm

# Create your views here.
def index(request):
    form = CitiesForm(initial={
      'first_city': request.GET.get('first_city'),
      'second_city': request.GET.get('second_city')
    })
    
    return render(request, "index.html", {
      'form': form,
    })