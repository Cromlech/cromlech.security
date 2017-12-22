# -*- coding: utf-8 -*-

from .interfaces import IProtectedComponent
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
                checker = IProtectedComponent(component)
                if checker is not None:
                    error = checker.__check_security__()
                    if error is not None:
                        raise error
            except ComponentLookupError:
                pass
        return component
    return protect_component
