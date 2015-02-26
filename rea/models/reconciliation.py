from django.db import models
from django.utils.functional import cached_property

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

    value = models.FloatField()

    # possibly can be determined automatically
    unbalanced_value = models.FloatField(default=0)

    # system user can override and declare reconciliation
    marked_reconciled = models.BooleanField(default=False)

    class Meta:
        ordering = ('-pk', )

    @cached_property
    def is_reconciled(self):
        unbalanced = self.value - sum(
            event.quantity for event in self.events.all()
        )

        if self.unbalanced_value != unbalanced:
            self.unbalanced_value = unbalanced
            self.save()

        return self.unbalanced_value == 0

    def save(self, *args, **kwargs):
        if not self.pk and not self.value:
            self.value = self.event.quantity

        super(Reconciliation, self).save(*args, **kwargs)


class ReconciliationInitiator(Reconciliation):
    '''
    The Initiator Reconciliation object should be related
    to a corresponding Terminator
    '''

    @cached_property
    def is_reconciled(self):
        reconciled = super(self.__class__, self).is_reconciled

        siblings = self.__class__.objects.filter(
            event=self.event,
            pk__lt=self.pk
        )

        if siblings.exists():
            return all(sibling.is_reconciled for sibling in siblings)

        return reconciled


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
