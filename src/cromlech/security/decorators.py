# -*- coding: utf-8 -*-

from .interfaces import ISecuredComponent
from .interaction import getInteraction
from zope.interface.interfaces import ComponentLookupError


def component_protector(lookup):
    """This decorator can be used on any lookup function.
    It provides a way to wrap the resulting component in a
    sticky security proxy, securing the component accesses.
    """
    def protect_component(*args, **kwargs):
        component = lookup(*args, **kwargs)
        if component is not None:
            try:
                checker = ISecuredComponent(component)
                interaction = getInteraction()                 
                checker.check(interaction)
            except ComponentLookupError:
                pass
        return component
    return protect_component
