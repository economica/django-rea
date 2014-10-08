from itertools import chain

from django.db import models

from . import REAObject


class Reconciliation(REAObject):
    '''
    Reconicile an Commitment or Event against other comparable
    Commitments or Events
    '''
    event = models.ForeignKey(
        'rea.Event',
        related_name='%(app_label)s_%(class)s_event')

    events = models.ManyToManyField(
        'rea.Event',
        related_name='%(app_label)s_%(class)s_events')

    value = models.FloatField()
    unbalanced_value = models.FloatField()

    is_reconciled = models.BooleanField(
        default=False)

    # def save(self):
    #     '''
    #     Check that all events are
    #     the same type of comparable Resource
    #     '''
    #     super(Reconciliation, self).save()

        # resource_class = self.event.resource.__class__
        # for event in self.events:
        #     if event.resource.__class__ != resource_class:
        #         return



class ReconciliationInitiator(Reconciliation):
    '''
    The Initiator Reconciliation object should be related
    to a corresponding Terminator
    '''
    terminator = models.ForeignKey(
        'ReconciliationTerminator',
        null=True
    )


class ReconciliationTerminator(Reconciliation):
    '''
    The Initiator Reconciliation object should be related
    to a corresponding Terminator
    '''
    initiator = models.ForeignKey(
        'ReconciliationInitiator',
        null=True
    )
