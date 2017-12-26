# -*- coding: utf-8 -*-

from .interfaces import ISecurityPredicate
from .interaction import getInteraction
from zope.interface.interfaces import ComponentLookupError


def security_predication(cls):
    """Does a subscription lookup from a class implementedBy.
    Does NOT raise, it just returns the error.
    """
    try:
        predicates = ISecurityPredicate.predicates(cls)
        if predicates is not None:
            interaction = getInteraction()
            for predicate in predicates:
                error = predicate(cls, interaction)
                if error is not None:
                    return error
    except ComponentLookupError:
        pass
