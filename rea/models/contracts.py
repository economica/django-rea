import logging

from django.db import models

from django_xworkflows import models as xwf_models
from polymorphic import PolymorphicModel

from entropy.base import (
    TextMixin, TitleMixin, CreatedMixin, ModifiedMixin, OrderingMixin
)

from ..settings import REA_RECEIVING_AGENT_MODEL, REA_PROVIDING_AGENT_MODEL


logger = logging.getLogger(__name__)

#
#
#   http://code.activestate.com/recipes/204197-solving-the-metaclass-conflict/
#   Fixes conflicts between two Meta classes
#
#
import inspect, types

############## preliminary: two utility functions #####################

def skip_redundant(iterable, skipset=None):
    "Redundant items are repeated items or items in the original skipset."
    if skipset is None: skipset = set()
    for item in iterable:
        if item not in skipset:
            skipset.add(item)
            yield item


def remove_redundant(metaclasses):
    skipset = set([types.ClassType])
    for meta in metaclasses: # determines the metaclasses to be skipped
        skipset.update(inspect.getmro(meta)[1:])
    return tuple(skip_redundant(metaclasses, skipset))

##################################################################
## now the core of the module: two mutually recursive functions ##
##################################################################

memoized_metaclasses_map = {}

def get_noconflict_metaclass(bases, left_metas, right_metas):
     """Not intended to be used outside of this module, unless you know
     what you are doing."""
     # make tuple of needed metaclasses in specified priority order
     metas = left_metas + tuple(map(type, bases)) + right_metas
     needed_metas = remove_redundant(metas)

     # return existing confict-solving meta, if any
     if needed_metas in memoized_metaclasses_map:
       return memoized_metaclasses_map[needed_metas]
     # nope: compute, memoize and return needed conflict-solving meta
     elif not needed_metas:         # wee, a trivial case, happy us
         meta = type
     elif len(needed_metas) == 1: # another trivial case
        meta = needed_metas[0]
     # check for recursion, can happen i.e. for Zope ExtensionClasses
     elif needed_metas == bases:
         raise TypeError("Incompatible root metatypes", needed_metas)
     else: # gotta work ...
         metaname = '_' + ''.join([m.__name__ for m in needed_metas])
         meta = classmaker()(metaname, needed_metas, {})
     memoized_metaclasses_map[needed_metas] = meta
     return meta

def classmaker(left_metas=(), right_metas=()):
    def make_class(name, bases, adict):
        metaclass = get_noconflict_metaclass(bases, left_metas, right_metas)
        return metaclass(name, bases, adict)
    return make_class


class ContractTemplate(PolymorphicModel, TitleMixin):
    '''
    Contract model which is instantiated by an Offer for Goods (Products) or Services
    in return for Payment or other form of Exchange Duality.

    Future features:
        - Visitor Pattern Override
        - Contract Versioning
    '''
    pass


class Contract(xwf_models.WorkflowEnabled, PolymorphicModel):
    '''
    A completely instantiated instance of a ContractTemplate that has become an
    immutable binding agreement between the participating Agents

    The Bound Contract model gains the Workflow functions; whilst the Contract model
    is more an abstract template.

    At time of intantiation a complete copy is made of the Contract.

    A bunch of logic could be placed here in the future to model other states
    that the contract might permeate.
    '''

    __metaclass__ = classmaker()

    receiving_agent = models.ForeignKey(
        REA_RECEIVING_AGENT_MODEL,
        related_name='%(app_label)s_%(class)s_receiving_agent'
    )
    providing_agent = models.ForeignKey(
        REA_PROVIDING_AGENT_MODEL,
        related_name='%(app_label)s_%(class)s_providing_agent'
    )

    def save(self, force=False):
        '''
        Once the BoundContract is saved once; it cannot be changed.

        We introcduce a `force` arguement to allow state changes to the contract beyond the
        management of the workflow
        '''
        if force:
            return super(BoundContract).save(self)
        if self.id:
            # @@@ this should be done better?
            raise Exception('A Bound Contract cannont be altered once created.  It must be recreated.')
        return super(BoundContract).save(self)


    is_terminated = models.BooleanField(default=False)

    def terminate(self):
        '''
        Forcibily terminate the contract; use with care.
        '''
        self.is_terminated = True
        self.save(force=True)

    def is_reciprocicated(self):
        '''
        What on earth did I have this function here for?
        '''
        return True

    def is_satisfied(self):
        return True
        # Loop through ordered Contract Clauses with their respective
        # Clause Rules.  If all pass, then the Contract is satisfied / fulfilled.
        # XXX implement logic.
        # XXX integrate with workflow states.


class Clause(PolymorphicModel, TitleMixin, TextMixin):
    '''
    A Clause is a reuseable set of one or more Clause Rules, attached
    by the ClauseRuleAspect pattern.

    '''
    # title
    # short_title
    pass


class ClauseRuleAspect(PolymorphicModel, CreatedMixin, ModifiedMixin):
    '''
    Attached to a Contract via through model ContractClause.  This model
    must be overridden with a provided `is_passing` method that returns True
    or False depending on the business logic required.

    '''

    # clause = models.ForeignKey(
    #     'Clause',
    #     related_name='%(app_label)s_%(class)s_clause'
    # )

    def is_passing(self):
        '''
        Test whether the current clause passes or fails. Returns
        either True or False.

        Usage:
            if clause_rule.is_passing:
                # do something...
        '''
        raise NotImplementedError(
            'Must override is_passing method for each rule')


class ContractClause(PolymorphicModel, OrderingMixin):
    '''
    Contract Clause

    '''
    # order / ordering

    contract = models.ForeignKey('Contract')
    clause = models.ForeignKey('Clause')


class ContractInstance(models.Model):
    pass


class ContractInstanceClause(PolymorphicModel, OrderingMixin):
    '''
    A full instantiated Contrace Instance Clause

    '''

    contract_instance = models.ForeignKey('ContractInstance')
    clause = models.ForeignKey('Clause')


#
# Clause Rules Library
#

class PaymentReceived(ClauseRuleAspect):

    def is_passing(self):
        return True
        # Logic here to determine whether a payment has been received.


class FulfilmentMade(ClauseRuleAspect):

    def is_passing(self):
        return True
        # Logic to determine the fulfilment of an Order
