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


class AggregatedAccount(Account):

    starting_balance = models.DecimalField(
        default=0.00,
        decimal_places=4,
        max_digits=13
    )

    def balance(self):

        # Sum the Increment Events subtracting the sum
        # of Decrement Events since the start of the accounting
        # period; for the given resource_type and given agent
        balance = self.starting_balance

        increment_events_qset = get_model('rea.IncrementEvent').objects.filter(receiving_agent=self.agent)
            # occured_at__gte=datetime.datetime(1970, 1, 1, 0, 0) # TODO this should be a setting or lookup value
            # )
        # import ipdb; ipdb.set_trace()

        increment_events = []

        for increment_event in increment_events_qset:
            if ContentType.objects.get_for_model(increment_event.resource) == self.resource_type:
                increment_events.append(increment_event)
                balance = Decimal(balance) + Decimal(increment_event.quantity)
                
                print 'increase {} {} giving {} in balance'.format(
                    increment_event.quantity,
                    self.resource_type,
                    balance)

        decrement_events_qset = get_model('rea.DecrementEvent').objects.filter(
            providing_agent=self.agent
            # occured_at__gte=datetime.datetime(1970, 1, 1, 0, 0) # TODO this should be a setting or lookup value
            )

        decrement_events = []

        for decrement_event in decrement_events_qset:
            if ContentType.objects.get_for_model(decrement_event.resource) == self.resource_type:
                decrement_events.append(decrement_event)
                balance = Decimal(balance) - Decimal(decrement_event.quantity)

                print 'decrease {} {} giving {} in balance'.format(
                    decrement_event.quantity,
                    self.resource_type,
                    balance)

        return balance


class ItemizedAccountResource(models.Model):

    account = models.ForeignKey('rea.ItemizedAccount')
    resource = models.ForeignKey('rea.ItemizedResource')


class ItemizedAccount(Account):

    def balance(self):
        '''
        Return a count of the Itemized Resources held in this account.
        '''
        balance = ItemizedAccountResource.objects.filter(account=self).count()

        increment_events_qset = get_model('rea.IncrementEvent').objects.filter(
            providing_agent=self.agent
            # occured_at__gte=datetime.datetime(1970, 1, 1, 0, 0) # TODO this should be a setting or lookup value
            )

        for increment_event in increment_events_qset:
            if ContentType.objects.get_for_model(increment_event.resource) == self.resource_type:
                balance -= increment_event.quantity
                print 'increase {} {}'.format(
                    self.resource_type,
                    balance
                    )


        decrement_events_qset = get_model('rea.DecrementEvent').objects.filter(
            providing_agent=self.agent
            # occured_at__gte=datetime.datetime(1970, 1, 1, 0, 0) # TODO this should be a setting or lookup value
            )

        for decrement_event in decrement_events_qset:
            if ContentType.objects.get_for_model(decrement_event.resource) == self.resource_type:
                balance -= decrement_event.quantity
                print 'decrease {} {}'.format(
                    self.resource_type,
                    balance
                    )


        print 'counted {} {}'.format(
            balance,
            self.resource_type)

        return balance

