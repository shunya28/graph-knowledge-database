from tokenize import String
from django.db import models
from neomodel import StructuredNode, StringProperty, UniqueIdProperty, RelationshipTo, StructuredRel


# Create your models here.
class Person(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True)

    # Relations :
    friends = RelationshipTo('Person', 'KNOWS')


# class ArticleRel(StructuredRel):
#     # uid = UniqueIdProperty()
#     uid_start = StringProperty()
#     uid_end = StringProperty()
# relationshipで設定した「参照」っていう文字列を取得したい時は、
# 最悪ここでクラスを継承して文字列のプロパティを持たせて、そこから
# 取得すれば実現できる
# それかdb.cyper_query()でtype(r)を取ってくる


class Article(StructuredNode):
    uid = UniqueIdProperty()
    title = StringProperty(unique_index=True, required=True)
    body = StringProperty(unique_index=True, required=True)
    # ref = RelationshipTo('Article', '参照', model=ArticleRel)
    ref = RelationshipTo('Article', '参照')
