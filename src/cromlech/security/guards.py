# -*- coding: utf-8 -*-

import threading
from .errors import Unauthorized, Forbidden
from .interfaces import IProtectedComponent, ISecurityPredicate
from .interaction import getInteraction
from zope.interface.interfaces import ComponentLookupError


def security_predication(cls, swallow_errors=False):
    """Does a subscription lookup from a class implementedBy.
    Returns the class if security is OK.
    """
    try:
        predicates = ISecurityPredicate.predicates(cls)
        if predicates is not None:
            interaction = getInteraction()
            for predicate in predicates:
                error = predicate(cls, interaction)
                if error is not None:
                    if not swallow_errors:
                        raise error
                    return None
    except ComponentLookupError:
        pass
    return cls


def security_check(component, swallow_errors=False):
    """Adapts the component to IProtectedComponent and runs a check.
    """
    try:
        checker = IProtectedComponent(component)
        if checker is not None:
            interaction = getInteraction()
            error = checker.__check_security__(interaction)
            if error is not None:
                if not swallow_errors:
                    raise error
                return None
    except ComponentLookupError:
        pass
    return component


class SecurityGuards(threading.local):
    check = None
    predict = None


security_guards = SecurityGuards()

    
def getSecurityGuards():
    return security_guards.predict, security_guards.check


def setSecurityGuards(predict, check):
    security_guards.predict = predict
    security_guards.check = check


class ContextualSecurityGuards(object):

    def __init__(self, predict, check):
        self.previous_state = getSecurityGuards()
        self.predict = predict
        self.check = check

    def __enter__(self):
        setSecurityGuards(self.predict, self.check)
        return getSecurityGuards()

    def __exit__(self, type, value, traceback):
        # We restore everything even if an error occured
        predict, check = getSecurityGuards()
        assert self.check is check and self.predict is predict, (
            'Security guards changed during runtime.')
        setSecurityGuards(*self.previous_state)
