from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from .settings import RECEIVING_AGENT_MODEL, PROVIDING_AGENT_MODEL


@python_2_unicode_compatible
class NameMixin(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class LineMixin(models.Model):
    '''
    Polymorphic Mixin for Increment and Decrement lines
    '''
    resource = models.ForeignKey('rea.Resource')
    quantity = models.DecimalField(max_digits=13, decimal_places=4)

    class Meta:
        abstract = True


class DecrementLineMixin(LineMixin):
    receiving_agent = models.ForeignKey(
        RECEIVING_AGENT_MODEL,
        related_name='%(app_label)s_%(class)s_reveiving_agents'
    )

    class Meta:
        abstract = True


class IncrementLineMixin(LineMixin):
    providing_agent = models.ForeignKey(
        PROVIDING_AGENT_MODEL,
        related_name='%(app_label)s_%(class)s_providing_agents'
    )

    class Meta:
        abstract = True
