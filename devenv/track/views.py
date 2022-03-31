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
    try:
        title = request.POST['title']
        body = request.POST['body']
    except(KeyError):
        pass
    else:
        testnode = Article(title=title, body=body)
        testnode.save()
    return HttpResponseRedirect(reverse('track:index'))


def delnode(request):
    try:
        uid = request.POST['uid']
    except(KeyError):
        pass
    else:
        node = Article.nodes.get(uid=uid)
        node.delete()
    return HttpResponseRedirect(reverse('track:index'))
