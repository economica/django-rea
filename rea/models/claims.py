from django.db import models

from django_xworkflows import models as xwf_models
from polymorphic import PolymorphicModel


class Claim(PolymorphicModel):
    '''
    Materlialised Claims take form in terms of Invoices which are used
    to communicate the economic state between two Agents.
    '''
    pass


    
