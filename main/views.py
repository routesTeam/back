from django.shortcuts import render

from .forms import CitiesForm

# Create your views here.
def index(request):
    form = CitiesForm()
    return render(request, "index.html", {'form': form})