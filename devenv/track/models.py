from django.db import models
from neomodel import (
    StructuredNode,
    StringProperty,
    UniqueIdProperty,
    IntegerProperty,
    DateTimeProperty,
    RelationshipTo,
    StructuredRel,
)


# Create your models here.
class Person(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True)

    # Relations :
    friends = RelationshipTo('Person', 'KNOWS')


class ArticleRel(StructuredRel):
    # uid = UniqueIdProperty()
    # uid_start = StringProperty()
    # uid_end = StringProperty()
    # TODO: どういう構造にするか考える
    pass
# relationshipで設定した「参照」っていう文字列を取得したい時は、
# 最悪ここでクラスを継承して文字列のプロパティを持たせて、そこから
# 取得すれば実現できる
# それかdb.cyper_query()でtype(r)を取ってくる


class Article(StructuredNode):
    uid = UniqueIdProperty()
    title = StringProperty(unique_index=True, required=True)
    body = StringProperty(unique_index=True, required=True)
    ref = RelationshipTo('Article', '参照', model=ArticleRel)

    # 第３引数が無いと「Relationship properties without using a relationship model is no longer supported.」ってneomodelに言われた
    # views.pyのconnect()でエラーraiseされるらしい
    # ref = RelationshipTo('Article', '参照')


# new experiment since 2022/6/21
class ArticleRel2(StructuredRel):
    creation_date = DateTimeProperty(default_now=True)
    likes = IntegerProperty(default=0)


class Article2(StructuredNode):
    creation_date = DateTimeProperty(default_now=True)
    # edit_date = DateTimeProperty()
    title = StringProperty(required=True)
    body = StringProperty(required=True)

    reference = RelationshipTo('Article2', 'refers_to', model=ArticleRel2)
    next_article = RelationshipTo('Article2', 'comes_before', model=ArticleRel2)
    related_tech = RelationshipTo('TechCategory', 'describes')  # , cardinality=OneOrMore)


class TechCategory(StructuredNode):
    name = StringProperty(required=True)

    # article = RelationshipFrom('Article2', 'describes', cardinality=OneOrMore)
    parent_tech = RelationshipTo('TechCategory', 'is_part_of')
    related_area = RelationshipTo('AreaCategory', 'is_part_of')


class AreaCategory(StructuredNode):
    name = StringProperty(required=True)
