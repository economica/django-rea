from django.db import models

from ..mixins import IncrementLineMixin, DecrementLineMixin

from .base import REAObject


class Event(REAObject):
    '''
    The REA Event object forms the Economic System Ledger.

    Every (economic) Event should have a corresponding Commitment (Line) to
    have made that Event; along with the container Contract which is implied
    by the relationship.
    '''

    occured_at = models.DateTimeField(auto_now_add=True)


class DecrementEvent(Event, DecrementLineMixin):
    '''
    DecrementEvent down cast from Event
    '''

    # reveiving_agent
    # occured_at
    # resource
    # quantity


class IncrementEvent(Event, IncrementLineMixin):
    '''
    IncrementEvent down cast from Event
    '''

    # providing_agent
    # occured_at
    # resource
    # quantity
