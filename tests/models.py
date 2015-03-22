from entropy.base import NameMixin, TitleMixin, SlugMixin

from rea.models import Agent, ItemizedResource, Resource


class Person(Agent, NameMixin, SlugMixin):
    '''
    Here is an Agent subclass
    '''
    pass


class Organisation(Agent, TitleMixin, SlugMixin):
    '''
    Here is another Agent subclass
    '''
    pass


class Product(ItemizedResource):
	pass


class Fish(Product):
	pass


class Currency(Resource):
	pass


class Cash(Currency):
	pass
