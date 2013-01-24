# -*- coding: utf-8 -*-

from zope.interface import implements
from .interfaces import IInteraction, IPrincipal, IProtagonist


class Interaction(set):
    implements(IInteraction)

    def __init__(self, protagonists, previous=None):
        self.previous = previous
        for protagonist in protagonists:
            self.add(protagonist)

    @property
    def principals(self):
        return set((p.principal for p in self))

    def add(self, protagonist):
        if protagonist.interaction is not None:
            raise ValueError(
                "%r already belongs to an interaction" % protagonist)

        protagonist.interaction = self
        set.add(self, protagonist)

    def remove(self, protagonist):
        if protagonist.interaction is not self:
            raise ValueError(
                "%r does not belong to this interaction" % protagonist)
        set.remove(self, protagonist)
        protagonist.interaction = None


class Protagonist(object):
    implements(IProtagonist)

    def __init__(self, principal):
        assert IPrincipal.providedBy(principal)
        self.principal = principal
        self.interaction = None
