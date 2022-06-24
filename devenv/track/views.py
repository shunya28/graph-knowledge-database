from platform import node
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Article
from django.views import View
from neomodel.exceptions import DoesNotExist
from neomodel import db, StructuredNode, StructuredRel


def index(request):
    # return render(request, 'track/index.html')
    # all_persons = Person.nodes.all()
    articles = Article.nodes.all()

    # https://stackoverflow.com/questions/67821341/retrieve-the-relationship-object-in-neomodel
    relationships = []
    for article in articles:
        for article_ref in article.ref:
            print(type(article_ref))
            relationships.append(article.ref.relationship(article_ref))

    # print(relationships)

    # from neomodel import db, StructuredRel
    # results, meta = db.cypher_query("match (n)-[r]->() return r")
    # print(results)
    # print(StructuredRel.inflate(results[0][0]).start_node())

    # for article in articles:
    #     print(article)

    # test_rels = articles[0].ref.all_relationships(articles[0].ref)
    # for article in articles:
    #     for j in range(len(articles)):
    #         print(type(article.nodes))
    #         # tmp = article.all_relationships(articles[j])
    #         # test_rels.append(tmp)

    # print(test_rels)
    
    # for relationship in relationships:
    #     print(relationship.name)
    #     print(dir(relationship))
        # print(relationship.id)
        # print(relationship.start_node())

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


# new experiment since 2022/6/21
class Index(LoginRequiredMixin, View):
    def get(self, request):

        nodes, meta = db.cypher_query('MATCH (n)-[]->() RETURN n')
        rels, meta = db.cypher_query('MATCH ()-[r]->() RETURN r')

        # nodes = [StructuredNode.inflate(row[0]) for row in nodes]
        rels = [StructuredRel.inflate(row[0]) for row in rels]
        # results, meta = db.cypher_query("match (n)-[r]->() return r")
        # print(results)
        # print(StructuredRel.inflate(results[0][0]).start_node())

        graph_list = []
        print(Article.inflate(nodes[0][0]))
        context = {}
        return render(request, 'track/index.html', context)
