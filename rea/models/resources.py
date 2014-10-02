from polymorphic import PolymorphicModel

from entropy.base import SlugMixin, TitleMixin


class Resource(PolymorphicModel, TitleMixin, SlugMixin):

    # title
    # short_title
    # slug

    pass
