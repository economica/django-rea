from django.db import models

from .base import REAObject


class Reconciliation(REAObject):
    '''
    Reconicile an Commitment or Event against other comparable
    Commitments or Events
    '''
    event = models.ForeignKey(
        'rea.Event',
        related_name='%(app_label)s_%(class)s_event'
    )

    events = models.ManyToManyField(
        'rea.Event',
        related_name='%(app_label)s_%(class)s_events'
    )

    # value is specified manually by system user
    value = models.FloatField()

    # possibly can be determined automatically
    unbalanced_value = models.FloatField()

    # system user can override and declare reconciliation
    marked_reconciled = models.BooleanField(default=False)

    def is_reconciled(self):
        return self.marked_reconciled or self.event.quantity == sum(
            [event.quantity for event in self.events.all()]
        )


class ReconciliationInitiator(Reconciliation):
    '''
    The Initiator Reconciliation object should be related
    to a corresponding Terminator
    '''
    pass


class ReconciliationTerminator(Reconciliation):
    '''
    The Terminator Reconciliation object may relate
    to many Initiators and vice versa
    '''
    initiators = models.ManyToManyField(
        'ReconciliationInitiator',
        related_name='terminators',
        null=True
    )
