# -*- coding: utf-8 -*-

from .interfaces import IPrincipal, IUnauthenticatedPrincipal
from zope.interface import implementer


ANONYMOUS = 'user.unauthenticated'


@implementer(IPrincipal)
class Principal(object):

    def __init__(self, id, title=u'', description=u''):
        self.id = id
        self.title = title
        self.description = description


@implementer(IUnauthenticatedPrincipal)
class UnauthenticatedPrincipal(object):

    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description
        self.groups = []


unauthenticated_principal = UnauthenticatedPrincipal(
    ANONYMOUS,
    u'Unauthenticated principal',
    u'The default unauthenticated principal.')
