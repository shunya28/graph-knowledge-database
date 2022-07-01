from platform import node
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


def addnode(request):
    # TODO: ここの例外処理要る？
    try:
        title = request.POST['title']
        body = request.POST['body']
        references = request.POST['references'].split(',')
    except(KeyError):
        pass
    else:
        node_to_add = Article(title=title, body=body)
        node_to_add.save()

        # FIXME: referencesが['']だとエラー吐く
        for ref_id in references:
            try:
                # node_to_connect = Article.nodes.get(id=ref_id)
                node_to_connect = db.cypher_query(f'MATCH (n) WHERE id(n) = {ref_id} RETURN n')
                # node_to_connect = Article.inflate(node_to_connect[0][0][0])
            except(DoesNotExist):
                # node_to_add.ref = None
                pass
            else:
                pass
                # print(type(Article.inflate(node_to_connect[0][0][0])))
                # node_to_add.reference.connect(node_to_connect[0][0][0])  # これがうまくいかないのでcypherで良いかも
                # node_to_add.ref.connect(node_to_connect,
                #                         {'uid_start': node_to_add.uid, 'uid_end': node_to_connect.uid})
        # node_to_add.refresh()はいらない？

    return HttpResponseRedirect(reverse('track:index'))


def delnode(request):
    try:
        id_list = request.POST['node-ids'].split(',')
        id_list = [int(id) for id in id_list]
    except(KeyError):
        pass
    else:
        db.cypher_query(f'MATCH (n) WHERE id(n) IN {id_list} DELETE n')

    return HttpResponseRedirect(reverse('track:index'))


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
