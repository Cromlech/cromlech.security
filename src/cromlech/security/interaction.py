# -*- coding: utf-8 -*-

import threading
from .errors import MissingSecurityContext
from .interfaces import IPrincipal, IProtagonist
from .components import Interaction, Protagonist
from .principal import unauthenticated_principal


class ThreadLocalSecurity(threading.local):
    """Session hook land.
    """
    interaction = None


thread_local_security = ThreadLocalSecurity()


def queryInteraction():
    return thread_local_security.interaction


def getInteraction():
    """this function disallows empty interactions
    """
    interaction = thread_local_security.interaction
    if interaction is None:
        raise MissingSecurityContext('No interaction.')
    return interaction


def setInteraction(interaction):
    previous = queryInteraction()
    if interaction is not None and interaction.previous is not None:
        interaction.previous = previous

    thread_local_security.interaction = interaction
    return thread_local_security.interaction


def removeFromInteraction(principal, interaction=None):
    if interaction is None:
        interaction = getInteraction()

    for protagonist in interaction:
        if protagonist.principal is principal:
            interaction.remove(protagonist)
            return True
    return False


def joinInteraction(principal, interaction=None):
    if interaction is None:
        interaction = getInteraction()

    if principal not in interaction.principals:
        protagonist = Protagonist(principal)
        interaction.add(protagonist)
        return True
    return False
        

def restoreInteraction():
    interaction = queryInteraction()
    if interaction is not None and interaction.previous is not None:
        thread_local_security.interaction = interaction.previous
    else:
        raise AssertionError(
            "No restorable interaction has been set.")


def deleteInteraction():
    thread_local_security.interaction = None


def newInteraction(*protagonists):
    """Start a new interaction.
    """
    interaction = queryInteraction()
    if interaction is not None:
        new_interaction = Interaction(protagonists, previous=interaction)
    else:
        new_interaction = Interaction(protagonists)
    setInteraction(new_interaction)
    return new_interaction


def endInteraction():
    """End the current interaction.
    """
    interaction = queryInteraction()
    if interaction is not None:
        if interaction.previous is not None:
            interaction = restoreInteraction()
        else:
            deleteInteraction()
            interaction = None
    return interaction


class ContextualInteraction(object):

    def __init__(self, *principals):
        if not principals:
            principals = (unauthenticated_principal,)
        self.protagonists = [Protagonist(p) for p in principals]
        self.current = None

    def __enter__(self):
        self.current = newInteraction(*self.protagonists)
        return self.current

    def __exit__(self, type, value, traceback):
        current = getInteraction()
        assert self.current is current, (
            'Security context has changed during the `Interaction`')
        endInteraction()


class ContextualProtagonist(object):

    def __init__(self, principal=unauthenticated_principal):
        assert IPrincipal.providedBy(principal)
        self.protagonist = Protagonist(principal)

    def __enter__(self):
        interaction = queryInteraction()
        if interaction is None:
            newInteraction(self.protagonist)
        else:
            interaction.add(self.protagonist)
        return self.protagonist

    def __exit__(self, type, value, traceback):
        current = getInteraction()
        assert self.protagonist.interaction is current, (
            'Security context has changed during the `Interaction`')
        current.remove(self.protagonist)
        if not len(current):
            endInteraction()
