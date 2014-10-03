import logging

from django.db import models

from django_xworkflows import models as xwf_models
from polymorphic import PolymorphicModel

from entropy.base import (
    TitleMixin, SlugMixin
)

from ..settings import REA_RECEIVING_AGENT_MODEL, REA_PROVIDING_AGENT_MODEL
from ..utils import classmaker

from .reconciliation import Reconciliation
from .commitments import *
from .events import *

logger = logging.getLogger(__name__)


class Contract(PolymorphicModel, TitleMixin, SlugMixin):

    # title
    # short_title
    # slug

    receiving_agent = models.ForeignKey(
        REA_RECEIVING_AGENT_MODEL,
        related_name='%(app_label)s_%(class)s_receiving_agent'
    )
    providing_agent = models.ForeignKey(
        REA_PROVIDING_AGENT_MODEL,
        related_name='%(app_label)s_%(class)s_providing_agent'
    )

    def is_done(self):



        return NotImplemented()


class SalesOrder(Contract):

    def is_done(self):
        '''
        Sales Order is considered done when Payment has been reconciled
        against the Sale and the Product has been fulfilled.
        '''

        commitments = self.commitment_set.all()
        for commitment in commitments:
            if commitment.__class__ == IncrementCommitment:

                try:
                    # import ipdb; ipdb.set_trace()
                    reconciliation = Reconciliation.objects.get(event=commitment)
                except Reconciliation.DoesNotExist:
                    return False

                return reconciliation.is_reconciled


        return False
