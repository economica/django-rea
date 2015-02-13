from django.test import TestCase
from rea.models import (
    Agent, 
    Commitment,
    DecrementCommitment, 
    DecrementEvent,
    Event,
    IncrementCommitment,
    IncrementEvent,
    Resource, 
    ReconciliationInitiator,
    ReconciliationTerminator,
    SalesOrder, 
)


class SimpleTestCase(TestCase):
    def test_addition(self):
        self.assertEqual(1 + 1, 2)


class SalesOrderTest(TestCase):
    def setUp(self):
        # Resources
        # XXX: Daryl, should resources have some concept of ownership? Do we do that wish
        # an event somewhere?  Brenton: Ownership is shown by Accounts, as in Chart of Accounts
        # XXX: How is initial state represented?
        self.fish = Resource.objects.create(name='Fish')
        self.cash = Resource.objects.create(name='AUD')

        # Agents
        self.daryl = Agent.objects.create(name='Daryl Antony', slug='daryl')
        self.brenton = Agent.objects.create(name='Brenton Cleeland', slug='brenton')


    def test_agent_creation(self):
        # OK, we should have two agents in our system at this point
        self.assertEqual(Agent.objects.count(), 2)


    def test_sales_order(self):
        fish_order = SalesOrder()
        
        fish_order.recipient = self.daryl  # Customer
        fish_order.provider = self.brenton # Reporting Agent
        fish_order.save()

        # Order should be incomplete
        self.assertFalse(fish_order.is_done())

        # Fish Commitment
        decrement_comittment = DecrementCommitment.objects.create(
            contract=fish_order,
            resource=self.fish, 
            quantity=3, 
            receiving_agent=self.daryl)
        
        # Cash Commitment
        increment_comittment = IncrementCommitment.objects.create(
            contract=fish_order,
            resource=self.cash, 
            quantity=9.95, 
            providing_agent=self.daryl)

        # Order should _still_ be incomplete
        self.assertFalse(fish_order.is_done())

        # Sometime in the future; the following events happen
        increment_event = IncrementEvent(**{
            'resource': self.cash,
            'providing_agent': self.daryl,
            'quantity': 9.95
            })
        increment_event.save()

        # Order should _still_ be incomplete
        self.assertFalse(fish_order.is_done())

        decrement_event = DecrementEvent(**{
            'resource': self.fish,
            'receiving_agent': self.daryl,
            'quantity': 3
            })
        decrement_event.save()

        # Order should _still_ be incomplete
        self.assertFalse(fish_order.is_done())

        reconcile_sale = ReconciliationInitiator(**{
            'event': increment_comittment,
            'value': 9.95,
            'unbalanced_value': 0
            })
        reconcile_sale.save()
        reconcile_sale.events.add(increment_event)
        reconcile_sale.save()

        self.assertTrue(reconcile_sale.is_reconciled())


        reconcile_payment = ReconciliationTerminator(**{
            'event': increment_event,
            'value': 9.95,
            'unbalanced_value': 0
            })
        reconcile_payment.save()
        reconcile_payment.events.add(increment_comittment)
        reconcile_payment.save()


        # Okay, OMG, the existance of these events means we're sorted
        self.assertTrue(fish_order.is_done())
