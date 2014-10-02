from django.test import TestCase
from rea.models import (Agent, SalesOrder, Resource, Commitment,
    IncrementCommitmentLine, DecrementCommitmentLine, Event)


class SimpleTestCase(TestCase):
    def test_addition(self):
        self.assertEqual(1 + 1, 2)


class SalesOrderTest(TestCase):
    def setUp(self):
        # Resources
        # XXX: Daryl, should resources have some concept of ownership? Do we do that wish
        # an event somewhere?
        # XXX: How is initial state represented?
        self.fish = Resource.objects.create(title='Fish')
        self.cash = Resource.objects.create(title='AUD')

        # Agents
        self.daryl = Agent.objects.create(title='Daryl Antony', slug='daryl')
        self.brenton = Agent.objects.create(title='Brenton Cleeland', slug='brenton')


    def test_agent_creation(self):
        # OK, we should have two agents in our system at this point
        self.assertEqual(Agent.objects.count(), 2)


    def test_sales_order(self):
        fish_order = SalesOrder()
        fish_order.receiving_agent = self.brenton   # why is this needed when our commitment duplicate this information?
        fish_order.providing_agent = self.daryl
        fish_order.save()

        # Order should be incomplete
        self.assertFalse(fish_order.is_done())

        # Fish Commitment
        increment_fish = IncrementCommitmentLine.objects.create(resource=self.fish, quantity=3, providing_agent=self.daryl)
        decrement_fish = DecrementCommitmentLine.objects.create(resource=self.fish, quantity=3, receiving_agent=self.brenton)

        fish_commitment = Commitment()
        fish_commitment.contract = fish_order
        fish_commitment.increment_line = increment_fish
        fish_commitment.decrement_line = decrement_fish
        fish_commitment.save()

        # Cash Commitment
        increment_cash = IncrementCommitmentLine.objects.create(resource=self.cash, quantity=9.95, providing_agent=self.brenton)
        decrement_cash = DecrementCommitmentLine.objects.create(resource=self.cash, quantity=9.95, receiving_agent=self.daryl)

        # XXX: Okay, there should be a OneToOne relationship in here somewhere to ensure that we can't have
        # commitments associated with multiple orders (or Events!)
        cash_commitment = Commitment()
        cash_commitment.contract = fish_order
        cash_commitment.increment_line = increment_cash
        cash_commitment.decrement_line = decrement_cash
        cash_commitment.save()

        # Order should _still_ be incomplete
        self.assertFalse(fish_order.is_done())

        # Create payment events, then we're locking it in
        Event(commitment=fish_commitment).save()
        Event(commitment=cash_commitment).save()

        # Okay, OMG, the existance of these events means we're sorted
        self.assertTrue(fish_order.is_done())
