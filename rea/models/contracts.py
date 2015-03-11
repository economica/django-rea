import logging

from django.db import models
from django.utils.functional import cached_property

from ..settings import (
    REPORTING_AGENT_MODEL,
    REPORTING_AGENT_ID,
    RECEIVING_AGENT_MODEL
)

from .base import REAObject
from .reconciliation import Reconciliation


logger = logging.getLogger(__name__)


class Contract(REAObject):
    '''
    The simplest form of an REA Contract binds Commitments
    that increase and decrease economic resource in corresponding
    outflows & inflows.

    The providing & receiving agents are implied by the commitment
    lines.

    The basic contract should specify at least the Reporting Agent
    of the system; as the provider of outflows; and Recipient Agent

    The `provider` defaults to the Reporting Agent model class & ID
    as specified in the rea.settings; which is optionally overriden
    during implementation.
    '''

    # Contract.provider
    provider = models.ForeignKey(
        REPORTING_AGENT_MODEL,
        default=REPORTING_AGENT_ID,
        related_name='%(app_label)s_%(class)s_providers'
    )

    # Contract.recipient
    recipient = models.ForeignKey(
        RECEIVING_AGENT_MODEL,
        related_name='%(app_label)s_%(class)s_recipients'
    )

    def is_done(self):
        raise NotImplemented(
            'Contract rules need to be provided during implementation'
        )


class SalesOrder(Contract):
    @cached_property
    def is_done(self):
        '''
        Sales Order is considered done when Payment has been reconciled
        against the Sale and the Product has been fulfilled.
        '''

        events = self.commitment_set.all()

        try:
            initiator = Reconciliation.objects.filter(
                event__in=events,
                reconciliationinitiator__isnull=False
            ).earliest()
            terminator = Reconciliation.objects.filter(
                event__in=events,
                reconciliationterminator__isnull=False
            ).earliest()
        except Reconciliation.DoesNotExist:
            # If SalesOrder lacks of either initiator or negotiator is not done
            return False

        return initiator.is_reconciled and terminator.is_reconciled


class Burndown(Contract):
    @cached_property
    def is_done(self):
        '''
        Burndown is considered done when Payment has been reconciled
        against the Labour and the Work has been fulfilled.
        '''

        events = self.commitment_set.all()

        try:
            initiator = Reconciliation.objects.filter(
                event__in=events,
                reconciliationinitiator__isnull=False
            ).earliest()
            terminator = Reconciliation.objects.filter(
                event__in=events,
                reconciliationterminator__isnull=False
            ).earliest()
        except Reconciliation.DoesNotExist:
            # If Burndown lacks of either initiator or negotiator is not done
            return False

        return initiator.is_reconciled and terminator.is_reconciled
