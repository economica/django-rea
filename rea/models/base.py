import uuidfield

from polymorphic import PolymorphicModel


class REAObject(PolymorphicModel):
    '''
    Base class for all REA Models with PolymorphicModel and uuid.

    Allows us to do:
        REAObject.objects.all()

    And get every REA object in the system, or alternatively do something like:
        REAObject.objects.filter(uuid='1i725drcfgq4b3304g8f35c342')

    To look up a specific object of unknown type.
    '''

    uuid = uuidfield.UUIDField(auto=True)
