from polymorphic import PolymorphicModel

from entropy.base import NameMixin, SlugMixin


class Agent(PolymorphicModel, NameMixin, SlugMixin):
    pass
