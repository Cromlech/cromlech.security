# -*- coding: utf-8 -*-

from cromlech.security.interfaces import IUnauthenticatedPrincipal

ANONYMOUS = 'user.unauthenticated'


class UnauthenticatedPrincipal(object):
    implements(IUnauthenticatedPrincipal)

    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description
        self.groups = []


unauthenticated_principal = UnauthenticatedPrincipal(
    ANONYMOUS,
    u'Unauthenticated principal',
    u'The default unauthenticated principal.')
