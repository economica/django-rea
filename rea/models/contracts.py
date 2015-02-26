import logging

from django.db import models

from ..settings import (
    REA_REPORTING_AGENT_MODEL,
    REA_REPORTING_AGENT_ID,
    REA_RECEIVING_AGENT_MODEL
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
        REA_REPORTING_AGENT_MODEL,
        default=REA_REPORTING_AGENT_ID,
        related_name='%(app_label)s_%(class)s_providers'
    )

    # Contract.recipient
    recipient = models.ForeignKey(
        REA_RECEIVING_AGENT_MODEL,
        related_name='%(app_label)s_%(class)s_recipients'
    )

    def is_done(self):
        raise NotImplemented(
            'Contract rules need to be provided during implementation'
        )


class SalesOrder(Contract):
    def is_done(self):
        '''
        Sales Order is considered done when Payment has been reconciled
        against the Sale and the Product has been fulfilled.
        '''

        reconciliations = []

        for commitment in self.commitment_set.all():
            try:
                reconciliation = Reconciliation.objects.get(
                    event=commitment
                )
            except Reconciliation.DoesNotExist:
                reconciliations.append(False)
            else:
                reconciliations.append(reconciliation.is_reconciled())

        return bool(reconciliations) and all(reconciliations)
