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

    value = models.DecimalField(
        default=0.00,
        decimal_places=4,
        max_digits=13
    )

    # possibly can be determined automatically
    unbalanced_value = models.DecimalField(
        default=0.00,
        decimal_places=4,
        max_digits=13
    )

    # system user can override and declare reconciliation
    marked_reconciled = models.BooleanField(default=False)

    class Meta:
        ordering = ('-pk', )
        get_latest_by = 'pk'

    @cached_property
    def is_reconciled(self):
        # We could use aggregation here, but since we're using polymorphic
        # classes we must get their actual class first
        unbalanced = self.value - sum(
            event.quantity for event in self.events.all()
        )

        if self.unbalanced_value != unbalanced:
            self.unbalanced_value = unbalanced
            self.save()

        try:
            # Get the next newer Reconciliation
            newer = self.__class__.objects.filter(
                event__commitment__contract=self.event.contract,
                pk__gt=self.pk
            ).earliest()
        except Reconciliation.DoesNotExist:
            return self.unbalanced_value == 0
        else:
            newer.value = self.unbalanced_value
            return newer.is_reconciled

    def save(self, *args, **kwargs):
        if not self.pk and not self.value:
            self.value = self.event.quantity

        super(Reconciliation, self).save(*args, **kwargs)


class ReconciliationInitiator(Reconciliation):
    '''
    The Initiator Reconciliation object should be related
    to a corresponding Terminator
    '''


class ReconciliationTerminator(Reconciliation):
    '''
    The Terminator Reconciliation object may relate
    to many Initiators and vice versa
    '''
    initiators = models.ManyToManyField(
        'ReconciliationInitiator',
        related_name='terminators'
    )
