from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Person, Article


# Create your views here.
def index(request):
    # return render(request, 'track/index.html')
    # all_persons = Person.nodes.all()
    all_articles = Article.nodes.all()
    context = {
        # 'nodes': all_persons,
        'nodes': all_articles,
    }

    return render(request, 'track/index.html', context)


def addnode(request):
    testnode = Article(title=request.POST['title'], body=request.POST['body'])
    testnode.save()
    return HttpResponseRedirect(reverse('track:index'))
