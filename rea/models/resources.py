from django.db import models

from ..mixins import NameMixin
from .base import REAObject


class Resource(REAObject, NameMixin):
    # name
    # uuid

    pass


class ItemizedResource(Resource):
    '''
    These Resources are individually trackable via a unique identifier
    such as a serial number.

    The affect Inventory Accounts by being tallied as a sum of Individual
    Resources; rather than the Aggregate of account history.
    '''

    # name
    # uuid

    serial = models.CharField(max_length=1024, unique=True)


class TimedResource(Resource):
    '''
    These resources have a duration, like Worked hours from an Agent or any
    other Resource consumed or used over time.
    '''

    class Unit:
        SECOND = 0
        MINUTE = 1
        HOUR = 2

    UNIT_CHOICES = (
        (Unit.SECOND, 'Seconds'),
        (Unit.MINUTE, 'Minutes'),
        (Unit.HOUR, 'Hours'),
    )

    # name
    # uuid

    quantity = models.FloatField()
    unit = models.SmallIntegerField(choices=UNIT_CHOICES, default=Unit.SECOND)
