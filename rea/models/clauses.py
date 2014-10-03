from polymorphic import PolymorphicModel


class Clause(PolymorphicModel, TitleMixin, TextMixin):
    '''
    A Clause is a reuseable set of one or more Clause Rules, attached
    by the ClauseRuleAspect pattern.

    '''
    # title
    # short_title
    contract_pattern = models.ForeignKey('ContractPattern')


class ClauseRuleAspect(PolymorphicModel):
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