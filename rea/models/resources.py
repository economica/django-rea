from django.db import models

from ..mixins import NameMixin
from .base import REAObject


class Resource(REAObject, NameMixin):
    pass


class ItemizedResource(Resource):
    '''
    These Resources are individually trackable via a unique identifier
    such as a serial number.

    The affect Inventory Accounts by being tallied as a sum of Individual
    Resources; rather than the Aggregate of account history.
    '''
    serial = models.CharField(max_length=1024, unique=True)
