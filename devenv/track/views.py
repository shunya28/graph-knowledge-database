from platform import node
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Person, Article
from neomodel.exceptions import DoesNotExist


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
        references = request.POST['references'].split(',')
    except(KeyError):
        pass
    else:
        node_to_add = Article(title=title, body=body)
        node_to_add.save()

        for ref_id in references:
            try:
                node_to_connect = Article.nodes.get(uid=ref_id)
            except(DoesNotExist):
                # node_to_add.ref = None
                pass
            else:
                node_to_add.ref.connect(node_to_connect)
        # node_to_add.refresh()はいらない？

    return HttpResponseRedirect(reverse('track:index'))


def delnode(request):
    try:
        uid = request.POST['uid']
    except(KeyError):
        pass
    else:
        node_to_delete = Article.nodes.get(uid=uid)
        node_to_delete.delete()
    return HttpResponseRedirect(reverse('track:index'))
