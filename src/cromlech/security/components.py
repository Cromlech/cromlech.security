# -*- coding: utf-8 -*-

from zope.interface import implements
from .interfaces import IInteraction, IProtagonist


class Interaction(set):
    implements(IInteraction)

    def __init__(self, participations, previous=None):
        self.previous = previous
        for participation in participations:
            self.add(participation)

    def add(self, participation):
        if participation.interaction is not None:
            raise ValueError(
                "%r already belongs to an interaction" % participation)

        participation.interaction = self
        set.add(self, participation)

    def remove(self, participation):
        if participation.interaction is not self:
            raise ValueError(
                "%r does not belong to this interaction" % participation)
        set.remove(self, participation)
        participation.interaction = None


class Protagonist(object):
    implements(IProtagonist)

    def __init__(self, principal):
        self.principal = principal
        self.interaction = None
