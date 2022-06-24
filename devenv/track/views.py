from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import (
    Article,
    Reference,
    Sequence,
    TechCategory,
    AreaCategory,
)
from django.views import View
from neomodel.exceptions import DoesNotExist
from neomodel import db, StructuredNode, StructuredRel

# deprecated
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
        uid_list = request.POST['uid'].split(',')
    except(KeyError):
        pass
    else:
        for uid in uid_list:
            node_to_delete = Article.nodes.get(uid=uid)
            node_to_delete.delete()

    return HttpResponseRedirect(reverse('track:index'))


# new experiment since 2022/6/21
class Index(LoginRequiredMixin, View):
    def get(self, request):

        nodes = self.get_all_nodes()
        rels = self.get_all_relationships()

        nodes = self.convert_node_to_dictlist(nodes)
        rels = self.convert_rel_to_dictlist(rels)

        graph_data = nodes + rels
        context = {
            'graph_data': graph_data
        }

        return render(request, 'track/index.html', context)

    # TODO: 一般化したい
    def get_all_nodes(self):

        # get all data from Neo4j database
        articles = db.cypher_query('MATCH (n:Article) RETURN n')
        techs = db.cypher_query('MATCH (n:TechCategory) RETURN n')
        areas = db.cypher_query('MATCH (n:AreaCategory) RETURN n')

        # change the Neo4j objects to neomodel objects
        articles = [Article.inflate(node[0]) for node in articles[0]]
        techs = [TechCategory.inflate(node[0]) for node in techs[0]]
        areas = [AreaCategory.inflate(node[0]) for node in areas[0]]

        nodes = articles + techs + areas
        return nodes

    def get_all_relationships(self):

        # get all data from Neo4j database
        raw_rels = db.cypher_query('MATCH ()-[r]->() RETURN r, type(r)')

        # change the Neo4j objects to neomodel objects
        # the shape is like:
        # [[<neomodel object>, 'TYPE_OF_R'], [...], [...
        rels = []
        for rel in raw_rels[0]:
            tmp = StructuredRel.inflate(rel[0])
            rels.append([tmp, rel[1]])

        return rels

    # TODO: 一般化したい
    def convert_node_to_dictlist(self, nodes):

        dict_list = []

        for node in nodes:
            prop_dict = {
                'data': {
                    'id': node.id,
                    'creation_date': node.creation_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'title': node.title,
                    'body': node.body
                }
            }
            dict_list.append(prop_dict)

        return dict_list

    def convert_rel_to_dictlist(self, rels):

        dict_list = []

        for rel in rels:
            prop_dict = {
                'data': {
                    'source': rel[0].start_node().id,
                    'target': rel[0].end_node().id,
                    'label': rel[1]
                }
            }
            dict_list.append(prop_dict)

        return dict_list
