import logging

from django.db import models

from django_xworkflows import models as xwf_models
from polymorphic import PolymorphicModel

from entropy.base import (
    TextMixin, TitleMixin, CreatedMixin, ModifiedMixin, OrderingMixin
)

from ..settings import REA_RECEIVING_AGENT_MODEL, REA_PROVIDING_AGENT_MODEL
from ..utils import classmaker

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

    def payment_recieved(self):
        pass

    def goods_fulfilled(self):
        pass

    def is_done(self):
        return self.payment_recieved() and self.goods_fulfilled()
