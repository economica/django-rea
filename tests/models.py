from entropy.base import NameMixin, TitleMixin, SlugMixin

from rea.models import Agent


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
