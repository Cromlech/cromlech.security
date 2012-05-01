# -*- coding: utf-8 -*-

from cromlech.security.components import Participation
from cromlech.security.principal import unauthenticated_principal
from zope.security.management import newInteraction, endInteraction
from zope.security.management import queryInteraction
from zope.security.interfaces import IPrincipal
from zope.security._definitions import thread_local


class Interaction(object):

    def __init__(self, principal=unauthenticated_principal, replace=True):
        assert IPrincipal.providedBy(principal)
        self.participation = Participation(principal)
        self.replace = replace
        self.previous = None
        self.current = None

    def __enter__(self):
        current = queryInteraction()
        new = self.participation

        if self.replace is False and current is not None:
            current.add(new)
        else:
            self.previous = current
            endInteraction()
            newInteraction(new)

        self.current = new.interaction
        return new.interaction

    def __exit__(self, type, value, traceback):
        current = queryInteraction()

        if self.current is not current:
            raise RuntimeError(
                'Security context has changed during the `Interaction`')
                               
        if self.replace is False:
            current.remove(self.participation)
        else:
            try:
                del thread_local.interaction
            except AttributeError:
                pass
            if self.previous is not None:
                thread_local.interaction  = self.previous
