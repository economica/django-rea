import decimal

from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

from rea.models import (
    AggregatedAccount,
    ItemizedAccount,
    ItemizedAccountResource,
    Burndown,
    DecrementCommitment,
    DecrementEvent,
    IncrementCommitment,
    IncrementEvent,
    Resource,
    ReconciliationInitiator,
    ReconciliationTerminator,
    SalesOrder,
    REAObject
)

from .models import *


class REAObjectTest(TestCase):
    def setUp(self):
        # 10
        for x in range(5):
            Person.objects.create()
            Resource.objects.create(name='Resource %s' % x)

        # 11
        self.order = SalesOrder.objects.create(**{
            'recipient': Person.objects.order_by('?')[0],
            'provider': Person.objects.order_by('?')[0]
        })

    def test_rea_object_selection(self):
        self.assertEqual(REAObject.objects.count(), 11)

    def test_object_selection(self):
        order = REAObject.objects.get(uuid=self.order.uuid)
        self.assertEqual(type(order), SalesOrder)

    def test_referential_integrity(self):
        with self.assertRaises(ValueError):
            # Should fail because providing_agent is an FK to the `rea.Agent`
            # type
            self.order.provider = Resource.objects.create(name='Fake Resource')


class SalesOrderTest(TestCase):
    def setUp(self):
    
        self.fish_one = Fish.objects.create(name='Fish one', serial='fish-one')
        self.fish_two = Fish.objects.create(name='Fish two', serial='fish-two')
        self.fish_three = Fish.objects.create(name='Fish three', serial='fish-three')

        self.cash = Cash.objects.create(name='AUD')

        # Agents
        self.daryl = Person.objects.create(
            name='Daryl Antony', 
            slug='daryl'
        )
        
        self.brenton = Person.objects.create(
            name='Brenton Cleeland',
            slug='brenton'
        )

        self.fish_account = ItemizedAccount.objects.create(
            agent=self.brenton,
            code='999',
            resource_type=ContentType.objects.get_for_model(Fish)
        )

        ItemizedAccountResource.objects.create(
            account=self.fish_account,
            resource=self.fish_one
        )

        ItemizedAccountResource.objects.create(
            account=self.fish_account,
            resource=self.fish_two
        )

        ItemizedAccountResource.objects.create(
            account=self.fish_account,
            resource=self.fish_three
        )

        self.cash_account = AggregatedAccount.objects.create(
            agent=self.brenton,
            code='888',
            starting_balance=0.00,
            resource_type=ContentType.objects.get_for_model(self.cash)
        )

        # Order
        self.order = SalesOrder.objects.create(
            recipient=self.daryl,  # Customer
            provider=self.brenton  # Reporting Agent
        )

    def test_agent_creation(self):
        # OK, we should have two agents in our system at this point
        self.assertEqual(Person.objects.count(), 2)

    def test_resource_creation(self):
        self.assertEqual(Resource.objects.count(), 4)

    def test_order_creation(self):
        # Order should be incomplete
        self.assertEqual(SalesOrder.objects.count(), 1)

    def test_reconciliation(self):

        decrement_commitment_one = DecrementCommitment.objects.create(
            contract=self.order,
            resource=self.fish_one,
            quantity=1,
            receiving_agent=self.daryl,
            providing_agent=self.brenton
        )

        decrement_commitment_two = DecrementCommitment.objects.create(
            contract=self.order,
            resource=self.fish_two,
            quantity=1,
            receiving_agent=self.daryl,
            providing_agent=self.brenton
        )

        decrement_commitment_three = DecrementCommitment.objects.create(
            contract=self.order,
            resource=self.fish_three,
            quantity=1,
            receiving_agent=self.daryl,
            providing_agent=self.brenton
        )

        s01 = DecrementEvent.objects.create(
            resource=self.fish_one,
            receiving_agent=self.daryl,
            providing_agent=self.brenton,
            quantity=1
        )

        s02 = DecrementEvent.objects.create(
            resource=self.fish_two,
            receiving_agent=self.daryl,
            providing_agent=self.brenton,
            quantity=1
        )

        s03 = DecrementEvent.objects.create(
            resource=self.fish_three,
            receiving_agent=self.daryl,
            providing_agent=self.brenton,
            quantity=1
        )

        initiator_01 = ReconciliationInitiator.objects.create(
            event=decrement_commitment_one
        )
        initiator_01.events.add(s01)
        initiator_01.save()


        initiator_02 = ReconciliationInitiator.objects.create(
            event=decrement_commitment_two
        )
        initiator_02.events.add(s02)
        initiator_02.save()


        initiator_03 = ReconciliationInitiator.objects.create(
            event=decrement_commitment_three
        )
        initiator_03.events.add(s03)
        initiator_03.save()


        # Cash Commitment
        increment_commitment = IncrementCommitment.objects.create(
            contract=self.order,
            resource=self.cash,
            quantity=9.95,
            providing_agent=self.daryl,
            receiving_agent=self.brenton
        )

        # Sometime in the future; the following events happen
        p01 = IncrementEvent.objects.create(
            resource=self.cash,
            providing_agent=self.daryl,
            receiving_agent=self.brenton,
            quantity=3.00
        )
        p02 = IncrementEvent.objects.create(
            resource=self.cash,
            providing_agent=self.daryl,
            receiving_agent=self.brenton,
            quantity=4.00
        )
        p03 = IncrementEvent.objects.create(
            resource=self.cash,
            providing_agent=self.daryl,
            receiving_agent=self.brenton,
            quantity=2.95
        )

        terminator_01 = ReconciliationTerminator.objects.create(
            event=increment_commitment
        )
        terminator_01.events.add(p01)
        terminator_01.initiators.add(initiator_01)
        terminator_01.save()

        terminator_02 = ReconciliationTerminator.objects.create(
            event=increment_commitment
        )
        terminator_02.events.add(p02, p03)
        terminator_02.initiators.add(initiator_02)
        terminator_02.save()

        # Okay, OMG, the existance of these events means we're sorted
        # self.assertTrue(self.order.is_done, 'SalesOrder is done')

        
        self.assertEqual(self.cash_account.balance(), decimal.Decimal('9.95'))
        self.assertEqual(self.fish_account.balance(), decimal.Decimal('0'))



class WorkedHoursTest(TestCase):
    def setUp(self):
        # Agents
        self.gam = Person.objects.create(name='Gamaliel', slug='gam')
        self.daz = Person.objects.create(name='Daryl', slug='daz')

        # Resources
        self.labour = Resource.objects.create(name='Labour')
        self.currency = Resource.objects.create(name='GBP')

        # Contracts
        self.burndown = Burndown.objects.create(
            recipient=self.gam,
            provider=self.daz
        )

        # Commitments
        self.commitments = {
            'decrement': [
                DecrementCommitment.objects.create(
                    contract=self.burndown,
                    resource=self.labour,
                    quantity=40,
                    receiving_agent=self.daz,
                    providing_agent=self.gam
                ),
                DecrementCommitment.objects.create(
                    contract=self.burndown,
                    resource=self.labour,
                    quantity=25,
                    receiving_agent=self.daz,
                    providing_agent=self.gam
                ),
                DecrementCommitment.objects.create(
                    contract=self.burndown,
                    resource=self.labour,
                    quantity=30,
                    receiving_agent=self.daz,
                    providing_agent=self.gam
                ),
                DecrementCommitment.objects.create(
                    contract=self.burndown,
                    resource=self.labour,
                    quantity=20,
                    receiving_agent=self.daz,
                    providing_agent=self.gam
                )
            ],
            'increment': [
                IncrementCommitment.objects.create(
                    contract=self.burndown,
                    resource=self.currency,
                    quantity=2000,
                    providing_agent=self.daz,
                    receiving_agent=self.gam
                ),
                IncrementCommitment.objects.create(
                    contract=self.burndown,
                    resource=self.currency,
                    quantity=2500,
                    providing_agent=self.daz,
                    receiving_agent=self.gam
                )
            ]
        }

    def test_agent_creation(self):
        self.assertEqual(Person.objects.count(), 2)

    def test_resource_creation(self):
        self.assertEqual(Resource.objects.count(), 2)

    def test_contract_creation(self):
        self.assertEqual(Burndown.objects.count(), 1)

    def test_decrement_commitment_ones_creation(self):
        self.assertEqual(DecrementCommitment.objects.count(), 4)

    def test_increment_commitments_creation(self):
        self.assertEqual(IncrementCommitment.objects.count(), 2)

    def test_burndown_contract_pattern(self):
        work = (
            DecrementEvent.objects.create(
                resource=self.labour,
                receiving_agent=self.daz,
                providing_agent=self.gam,
                quantity=8
            ),
            DecrementEvent.objects.create(
                resource=self.labour,
                receiving_agent=self.daz,
                providing_agent=self.gam,
                quantity=7
            ),
            DecrementEvent.objects.create(
                resource=self.labour,
                receiving_agent=self.daz,
                providing_agent=self.gam,
                quantity=10
            ),
            DecrementEvent.objects.create(
                resource=self.labour,
                receiving_agent=self.daz,
                providing_agent=self.gam,
                quantity=8
            ),
            DecrementEvent.objects.create(
                resource=self.labour,
                receiving_agent=self.daz,
                providing_agent=self.gam,
                quantity=7
            ),
            # 40 hours worked

            DecrementEvent.objects.create(
                resource=self.labour,
                receiving_agent=self.daz,
                providing_agent=self.gam,
                quantity=8
            ),
            DecrementEvent.objects.create(
                resource=self.labour,
                receiving_agent=self.daz,
                providing_agent=self.gam,
                quantity=10
            ),
            DecrementEvent.objects.create(
                resource=self.labour,
                receiving_agent=self.daz,
                providing_agent=self.gam,
                quantity=7
            ),
            DecrementEvent.objects.create(
                resource=self.labour,
                receiving_agent=self.daz,
                providing_agent=self.gam,
                quantity=10
            ),
            # 40 + 35 hours worked

            DecrementEvent.objects.create(
                resource=self.labour,
                receiving_agent=self.daz,
                providing_agent=self.gam,
                quantity=8
            ),
            DecrementEvent.objects.create(
                resource=self.labour,
                receiving_agent=self.daz,
                providing_agent=self.gam,
                quantity=7
            ),
            DecrementEvent.objects.create(
                resource=self.labour,
                receiving_agent=self.daz,
                providing_agent=self.gam,
                quantity=10
            ),
            DecrementEvent.objects.create(
                resource=self.labour,
                receiving_agent=self.daz,
                providing_agent=self.gam,
                quantity=8
            ),
            DecrementEvent.objects.create(
                resource=self.labour,
                receiving_agent=self.daz,
                providing_agent=self.gam,
                quantity=7
            )
            # 40 + 35 + 40 hours worked
        )

        payments = (
            IncrementEvent.objects.create(
                resource=self.currency,
                providing_agent=self.daz,
                receiving_agent=self.gam,
                quantity=750
            ),
            IncrementEvent.objects.create(
                resource=self.currency,
                providing_agent=self.daz,
                receiving_agent=self.gam,
                quantity=750
            ),
            IncrementEvent.objects.create(
                resource=self.currency,
                providing_agent=self.daz,
                receiving_agent=self.gam,
                quantity=1500
            ),
            IncrementEvent.objects.create(
                resource=self.currency,
                providing_agent=self.daz,
                receiving_agent=self.gam,
                quantity=500
            ),
            IncrementEvent.objects.create(
                resource=self.currency,
                providing_agent=self.daz,
                receiving_agent=self.gam,
                quantity=1000
            )
        )

        initiators = (
            ReconciliationInitiator.objects.create(
                event=self.commitments['decrement'][0]
            ),
            ReconciliationInitiator.objects.create(
                event=self.commitments['decrement'][1]
            ),
            ReconciliationInitiator.objects.create(
                event=self.commitments['decrement'][2]
            ),
            ReconciliationInitiator.objects.create(
                event=self.commitments['decrement'][3]
            )
        )
        initiators[0].events.add(*work[0:4])
        initiators[1].events.add(*work[4:8])
        initiators[2].events.add(*work[8:11])
        initiators[3].events.add(*work[11:])
        (initiator.save() for initiator in initiators)

        terminators = (
            ReconciliationTerminator.objects.create(
                event=self.commitments['increment'][0]
            ),
            ReconciliationTerminator.objects.create(
                event=self.commitments['increment'][1]
            )
        )
        terminators[0].events.add(*payments[0:2])
        terminators[0].initiators.add(*initiators[0:2])
        terminators[1].events.add(*payments[2:])
        terminators[1].initiators.add(*initiators[2:])
        (terminator.save() for terminator in terminators)

        self.assertTrue(self.burndown.is_done, 'Burndown Contract is done')
