# -*- coding: utf-8 -*-

from zope.security.interfaces import IGroupAwarePrincipal


class IUnauthenticatedPrincipal(IGroupAwarePrincipal):
    pass
