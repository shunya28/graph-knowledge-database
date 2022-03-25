from django.shortcuts import render
from .models import Person

# Create your views here.
def index(request):
    # return render(request, 'track/index.html')
    all_persons = Person.nodes.all()
    context = {
        'nodes': all_persons,
    }

    return render(request, 'track/index.html', context)
