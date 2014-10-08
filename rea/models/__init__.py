import uuidfield

from django.db import models
from polymorphic import PolymorphicModel

from ..settings import *


class REAObject(PolymorphicModel):
    '''
    Base class for all REA Models with PolymorphicModel and uuid.

    Allows us to do:
        REAObject.objects.all()

    And get every REA object in the system, or alternatively do something like:
        REAObject.objects.filter(uuid='1i725drcfgq4b3304g8f35c342')

    To look up a specific object of unknown type.
    '''
    uuid = uuidfield.UUIDField(auto=True)


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
