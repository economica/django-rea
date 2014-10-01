from polymorphic import PolymorphicModel

from entropy.base import SlugMixin, TitleMixin


class Agent(PolymorphicModel, SlugMixin, TitleMixin):
    pass
