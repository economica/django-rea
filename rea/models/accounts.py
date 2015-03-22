import datetime
from decimal import Decimal

from django.db import models
from django.db.models.loading import get_model
from django.contrib.contenttypes.models import ContentType

from django_xworkflows import models as xwf_models
from polymorphic import PolymorphicModel


ACCOUNTABLE_RESOURCES = ['resource',]


class Account(PolymorphicModel):
    '''
    Instantiate Accounts
    '''

    # An account code field to be consistent with 
    # accounting practices.
    code = models.CharField(max_length=255)

    agent = models.ForeignKey('rea.Agent')

    resource_type = models.ForeignKey(
        'contenttypes.ContentType',
        limit_choices_to=ACCOUNTABLE_RESOURCES)


    def balance(self):

        balance = self.starting_balance
        
        from itertools import chain
        
        events = list(chain(
            get_model('rea.IncrementEvent').objects.filter(receiving_agent=self.agent),
            get_model('rea.DecrementEvent').objects.filter(providing_agent=self.agent)
            )
        )

        for event in events:

            if ContentType.objects.get_for_model(event.resource) == self.resource_type:
                
                if event._meta.model == get_model('rea.IncrementEvent'):
                    balance = Decimal(balance) + Decimal(event.quantity)
                    operand = 'increase'
                else:
                    balance = Decimal(balance) - Decimal(event.quantity)
                    operand = 'decrease'
                             
                print '{} {} {} giving {} in balance'.format(
                    operand,
                    event.quantity,
                    self.resource_type,
                    balance)

        return balance


class AggregatedAccount(Account):

    starting_balance = models.DecimalField(
        default=0.00,
        decimal_places=4,
        max_digits=13
    )


class ItemizedAccountResource(models.Model):

    account = models.ForeignKey('rea.ItemizedAccount')
    resource = models.ForeignKey('rea.ItemizedResource')


class ItemizedAccount(Account):

    @property
    def starting_balance(self):
        return ItemizedAccountResource.objects.filter(account=self).count()
