from django.db import models

from . import REAObject

from entropy.base import NameMixin, SlugMixin


class Resource(REAObject, NameMixin, SlugMixin):
    pass


class ItemizedResource(Resource):
    '''
    These Resources are individually trackable via a unique identifier
    such as a serial number.

    The affect Inventory Accounts by being tallied as a sum of Individual 
    Resources; rather than the Aggregate of account history.
    '''
    serial = models.CharField(
        max_length=1024,
        unique=True)

