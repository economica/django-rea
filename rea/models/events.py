from django.db import models
from django.utils.functional import cached_property

from polymorphic import PolymorphicModel

from . import IncrementLineMixin, DecrementLineMixin
from ..settings import *


class Event(PolymorphicModel):
    '''
    The REA Event object forms the Economic System Ledger.

    Every (economic) Event should have a corresponding Commitment (Line) to have made that
    Event; along with the container Contract which is implied by the relationship.
    '''
    commitment = models.ForeignKey(
        'rea.Commitment',
        related_name='%(app_label)s_%(class)s_commitment')

    occured_at = models.DateTimeField(
        auto_now_add=True
    )

    def contract(self):
        return self.commitment.contract # @@@ is this necessary?

    @cached_property # its worth saving the instance on this for the life of the singleton
    def duality_event(self):
        try:
            # Fetch the Reciprocal Commitment and test
            # for the existence of a corresponding Increment or
            # Decrement Event

            commitment = self.commitment_line.commitment
            if commitment.decrement_line == self.commitment_line:
                # if we have a match; then we want the opposite;
                # we capture that below
                reciprocal_commitment_line = commitment.increment_line
            else:
                # otherwise we take the decrement line as the reciprocal
                reciprocal_commitment_line = commitment.decrement_line

            # Now try to find the matching Event duality
            return Event.objects.get({
                'commitment': commitment, # working with the same comitment object
                'providing_agent': reciprocal_commitment_line.providing_agent,
                'receiving_agent': reciprocal_commitment_line.receiving_agent,
                'resource': reciprocal_commitment_line.resource
                })

        except Event.DoesNotExist:
            return False


    def has_duality(self):
        '''
        Test whether the Decrement and / or Increment Events
        exist and satisfy the Duality of the exchange dictated by
        the Reciprocity of the Commitment.

        Not 100% sure if this function is useful; or merely theoretical;
        it's likely that with further knowledge, this will be overwritten
        to encapsulate proper Payment & Receipt reconcilliation logics
        found in Accounting systems.

        Upon more thinking, its likely that this function will get much more
        complex, dependending on reconcilliation logic - such as allowing for
        one or more applied payments to the initial provision of resources.
        '''
        dualtity_event = self.dualtity_event()
        if dualtity_event:
            return duality_event.quantity == self.quantity # @@@ fancy this line up some.
        # @@@ if we're returning False here; then we should be creating another
        # state; such as partially fulfilled.
        return False


class DecrementEvent(Event, DecrementLineMixin):
    '''
    DecrementEvent down cast from Event
    '''

    # reveiving_agent
    # commitment
    # occured_at
    # resource
    # quantity

    def commitment_line(self): # @@@ is this necessary?
        '''return the relevant commitment line'''
        return self.commitment.decrement_line


class IncrementEvent(Event, IncrementLineMixin):
    '''
    IncrementEvent down cast from Event
    '''

    # providing_agent
    # commitment
    # occured_at
    # resource
    # quantity

    def commitment_line(self): # @@@ is this necessary?
        '''return the relevant commitment line'''
        return self.commitment.increment_line
