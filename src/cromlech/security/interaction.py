# -*- coding: utf-8 -*-

from cromlech.security.principal import unauthenticated_principal
from zope.security.management import newInteraction, endInteraction


class Interaction(object):

    def __enter__(self, principal=unauthenticated_principal):
        newInteraction(Participation(principal))
        return principal

    def __exit__(self, type, value, traceback):
        endInteraction()
