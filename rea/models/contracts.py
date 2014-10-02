import logging

from django.db import models

from django_xworkflows import models as xwf_models
from polymorphic import PolymorphicModel

from entropy.base import (
    TitleMixin, SlugMixin
)

from ..settings import REA_RECEIVING_AGENT_MODEL, REA_PROVIDING_AGENT_MODEL
from ..utils import classmaker
from ..models import Event

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
        # For a sales order to be considered `Done` it needs commitments, and all of it's commitments
        # need to have matching `Event` objects
        commitments = self.commitment_set.all()

        # if there are no commitments, this can't be completed yet
        if not commitments:
            return False

        for c in commitments:
            if not Event.objects.filter(commitment=c):
                # return False immediately if we find a commitment without a matching Event
                return False

        return True
