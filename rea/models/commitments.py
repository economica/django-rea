from django.db import models

from . import IncrementLineMixin, DecrementLineMixin


class IncrementCommitmentLine(IncrementLineMixin):
    '''
    The Increment Commitment Line depicts an increase in Resource to 
    the Economic Agent that is the protagonist of the Economic system.

    The Increment Line is usually modelled from the perspective of the 
    Providing Agent / Reporting Agent
    '''
    # resource
    # quantity
    # providing_agent
    pass

class DecrementCommitmentLine(DecrementLineMixin):
    '''
    The Decrement Commitment Line depicts a decrease in Resource to the
    Reporting Agent, however, we specify the Receiving Agent or Recipient
    of the Resource; e.g. the Customer
    '''
    # resource
    # quantity
    # receiving_agent
    pass

class Commitment(models.Model):
    '''
    The Commitment model expresses a future reciprocity of the 
    Economic Event between two Agents.

    The Commitment object is related to a Contract instance
    which is a Workflow or Finite State Machine model.

    The Comittment object differs from the Event object in that 
    it houses the Reciprocity of the Commitment Increment Line && 
    the Commitment Decrement Line in an instantiated expresion of that
    Reciprocity.

    This is because a Commitment Increment & Decrement can be made
    simultaneously; and should be done so when entering into a BoundingContract.

    The resulting Increment and / or Decrement Events that will ultimately
    create the Event Exchange Duality to satisfy the Commitment Reciprocity 
    may occur at indetermined times into the future.

    The Contract workflow logic should provide mechanisms to check for corresponding
    duality by calling the Event 'has_duality' methods; or its overrides; and progressing
    the Contract workflow, according to its new state.
    '''

    contract = models.ForeignKey('rea.Contract')

    occured_at = models.DateTimeField(
        auto_now_add=True
    )

    increment_line = models.ForeignKey(
        IncrementCommitmentLine,
        related_name='%(app_label)s_%(class)s_increment_commitment_lines'
    )

    decrement_line = models.ForeignKey(
        DecrementCommitmentLine,
        related_name='%(app_label)s_%(class)s_decrement_commitment_lines'
    )
