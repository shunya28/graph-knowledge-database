from tokenize import String
from django.db import models
from neomodel import (
    StructuredNode,
    StringProperty,
    UniqueIdProperty,
    IntegerProperty,
    DateTimeProperty,
    DateTimeFormatProperty,
    RelationshipTo,
    StructuredRel,
)


class Reference(StructuredRel):
    creation_date = DateTimeProperty(default_now=True)
    likes = IntegerProperty(default=0)


class Sequence(StructuredRel):
    creation_date = DateTimeProperty(default_now=True)
    likes = IntegerProperty(default=0)


class Article(StructuredNode):
    creation_date = DateTimeProperty(default_now=True)
    # creation_date = DateTimeFormatProperty(default_now=True, format='%Y-%m-%d %H:%M:%S')
    # edit_date = DateTimeProperty()
    author = StringProperty()
    title = StringProperty(required=True)
    body = StringProperty(required=True)

    reference = RelationshipTo('Article', 'refers_to', model=Reference)
    next_article = RelationshipTo('Article', 'next', model=Sequence)
    related_tech = RelationshipTo('TechCategory', 'describes')  # , cardinality=OneOrMore)


class TechCategory(StructuredNode):
    name = StringProperty(required=True)

    # article = RelationshipFrom('Article2', 'describes', cardinality=OneOrMore)
    parent_tech = RelationshipTo('TechCategory', 'is_part_of')
    related_area = RelationshipTo('AreaCategory', 'is_part_of')


class AreaCategory(StructuredNode):
    name = StringProperty(required=True)
