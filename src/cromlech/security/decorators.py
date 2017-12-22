# -*- coding: utf-8 -*-

import threading
from .errors import SecurityException
from .interfaces import IProtectedComponent
from .interaction import getInteraction
from zope.interface.interfaces import ComponentLookupError


def no_security(lookup):
    return lookup


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
                    interaction = getInteraction()
                    error = checker.__check_security__(interaction)
                    if error is not None:
                        raise error
            except ComponentLookupError:
                pass
        return component
    return protect_component


class SecureLookup(threading.local):
    wrapper = None
    exceptions = None


secure_lookup = SecureLookup()
secure_lookup.wrapper = component_protector
secure_lookup.exceptions = (ComponentLookupError, SecurityException)


def getSecureLookup():
    return secure_lookup.wrapper, secure_lookup.exceptions


def setSecureLookup(wrapper, exceptions):
    secure_lookup.wrapper = wrapper
    secure_lookup.exceptions = exceptions


class ContextualSecurityWrapper(object):

    def __init__(self, wrapper):
        self.previous = getSecureLookup()
        self.wrapper = wrapper

    def __enter__(self):
        setSecureLookup(self.wrapper)
        return getSecureLookup()

    def __exit__(self, type, value, traceback):
        # We restore everything even if an error occured
        current = getSecureLookup()
        assert self.wrapper is current, (
            'Security wrapper has changed during runtime')
        setSecureLookup(self.previous)
