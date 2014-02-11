# -*- coding: utf-8 -*-

from zope.security.proxy import ProxyFactory


def component_protector(lookup):
    """This decorator can be used on any lookup function.
    It provides a way to wrap the resulting component in a
    sticky security proxy, securing the component accesses.
    """
    def protect_component(*args, **kwargs):
        component = lookup(*args, **kwargs)
        if component is not None:
            return ProxyFactory(component)
        return component
    return protect_component
