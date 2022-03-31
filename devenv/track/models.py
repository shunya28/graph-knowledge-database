from django.db import models
from neomodel import StructuredNode, StringProperty, UniqueIdProperty, RelationshipTo


# Create your models here.
class Person(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True)

    # Relations :
    friends = RelationshipTo('Person', 'KNOWS')


class Article(StructuredNode):
    uid = UniqueIdProperty()
    title = StringProperty(unique_index=True, required=True)
    body = StringProperty(unique_index=True, required=True)
    ref = RelationshipTo('Article', '参照')
