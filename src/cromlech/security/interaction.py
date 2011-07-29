# -*- coding: utf-8 -*-

from cromlech.security.components import Participation
from cromlech.security.principal import unauthenticated_principal
from zope.security.management import newInteraction, endInteraction


class Interaction(object):

    def __init__(self, principal=unauthenticated_principal):
        self.principal = principal

    def __enter__(self):
        newInteraction(Participation(self.principal))
        return self.principal

    def __exit__(self, type, value, traceback):
        endInteraction()
