from django.db import models

from ..settings import *


class LineMixin(models.Model):
    '''
    Polymorphic Mixin for Increment and Decrement lines
    '''
    resource = models.ForeignKey('rea.Resource')
    quantity = models.FloatField()

    class Meta:
        abstract = True


class DecrementLineMixin(LineMixin):

    receiving_agent = models.ForeignKey(
        REA_RECEIVING_AGENT_MODEL,
        related_name='%(app_label)s_%(class)s_reveiving_agents')

    class Meta:
        abstract = True


class IncrementLineMixin(LineMixin):

    providing_agent = models.ForeignKey(
        REA_PROVIDING_AGENT_MODEL,
        related_name='%(app_label)s_%(class)s_providing_agents')

    class Meta:
        abstract = True


from .events import *
from .contracts import *
from .agents import *
from .commitments import *
from .resources import *
from .reconciliation import *
from ..settings import REA_RECEIVING_AGENT_MODEL, REA_PROVIDING_AGENT_MODEL
