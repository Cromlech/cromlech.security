# -*- coding: utf-8 -*-

from zope.interface import implements
from zope.security.interfaces import IParticipation


class Participation(object):
    implements(IParticipation)

    def __init__(self, principal):
        self.principal = principal
        self.interaction = None
