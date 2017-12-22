# -*- coding: utf-8 -*-

from crom import component, target, sources
from .meta import permissions
from .interfaces import IProtectedComponent, IProtector, ISecurityCheck
from .interaction import queryInteraction


@component
@target(IProtector)
@sources(IProtectedComponent)
def base_protection(component):
    interaction = queryInteraction()
    checkers = ISecurityCheck.subscription(component)
    
    for checker in checkers:
        try:
            perms = frozenset(permissions.get(component) or tuple())
            checker(component, interaction, perms)
        except Exception as error:
            return error
    return None
