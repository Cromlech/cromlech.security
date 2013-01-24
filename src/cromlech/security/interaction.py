# -*- coding: utf-8 -*-

import threading
from .errors import MissingSecurityContext
from .interfaces import IPrincipal
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
    previous = getInteraction()
    if interaction is not None and interaction.previous is not None:
        interaction.previous = previous

    thread_local_security.interaction = interaction
    return thread_local_security.interaction


def restoreInteraction():
    interaction = getInteraction()
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
    interaction = getInteraction()
    if interaction is not None:
        new_interaction = Interaction(protagonists, previous=interaction)
    else:
        new_interaction = Interaction(protagonists)
    setInteraction(new_interaction)
    return new_interaction


def endInteraction():
    """End the current interaction.
    """
    interaction = getInteraction()
    if interaction is not None:
        if interaction.previous is not None:
            interaction = restoreInteraction()
        else:
            deleteInteraction()
            interaction = None
    return interaction


class ContextualInteraction(object):

    def __init__(self, principal=unauthenticated_principal, replace=True):
        assert IPrincipal.providedBy(principal)
        self.protagonist = Protagonist(principal)
        self.current = None

    def __enter__(self):
        self.current = newInteraction(self.protagonist)
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
        interaction = getInteraction()
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
