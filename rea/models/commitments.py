from django.db import models

from . import IncrementLineMixin, DecrementLineMixin
from .events import Event


class Commitment(Event):
    '''
    The Commitment model expresses a future reciprocity of the 
    Economic Event between two Agents.

    The Commitment object is related to a Contract instance
    which is a Workflow or Finite State Machine model.

    The Comittment object differs from the Event object in that 
    it houses the Reciprocity of the Commitment Increment Line && 
    the Commitment Decrement Line in an instantiated expresion of that
    Reciprocity.
    '''

    # occured_at

    contract = models.ForeignKey('rea.Contract')


class IncrementCommitment(Commitment, IncrementLineMixin):
    '''
    The Increment Commitment Line depicts an increase in Resource to 
    the Economic Agent that is the protagonist of the Economic system.

    The Increment Line is usually modelled from the perspective of the 
    Providing Agent / Reporting Agent
    '''

    # occured_at
    # contract
    # resource
    # quantity
    # providing_agent

    def is_reconciled():
        raise NotImplemented


class DecrementCommitment(Commitment, DecrementLineMixin):
    '''
    The Decrement Commitment Line depicts a decrease in Resource to the
    Reporting Agent, however, we specify the Receiving Agent or Recipient
    of the Resource; e.g. the Customer
    '''

    # occured_at
    # contract
    # resource
    # quantity
    # receiving_agent

    def is_fulfilled():
        raise NotImplemented
