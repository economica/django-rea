from entropy.base import NameMixin, SlugMixin

from .base import REAObject


class Agent(REAObject, NameMixin, SlugMixin):
    pass
