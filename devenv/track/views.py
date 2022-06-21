from platform import node
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Article
from neomodel.exceptions import DoesNotExist


# Create your views here.
def index(request):
    # return render(request, 'track/index.html')
    # all_persons = Person.nodes.all()
    articles = Article.nodes.all()

    # https://stackoverflow.com/questions/67821341/retrieve-the-relationship-object-in-neomodel
    relationships = []
    for article in articles:
        for article_ref in article.ref:
            relationships.append(article.ref.relationship(article_ref))

    # for article in articles:
    #     print(article.uid)
    
    # for relationship in relationships:
    #     print(relationship.name)
    #     print(dir(relationship))
    #     print(relationship)

    context = {
        # 'nodes': all_persons,
        'nodes': articles,
        'edges': relationships,
        # 'node_ids': [article.uid for article in articles],
        # 'data': [article.get_param_for_neo4j() for article in articles],
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
                node_to_add.ref.connect(node_to_connect,
                                        {'uid_start': node_to_add.uid, 'uid_end': node_to_connect.uid})
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
