# -*- coding: utf-8 -*-

from .components import Protagonist, Interaction
from .guards import ContextualSecurityGuards
from .guards import getSecurityGuards, setSecurityGuards
from .guards import security_check, security_predication
from .errors import SecurityException
from .errors import Unauthorized, Forbidden, MissingSecurityContext
from .interaction import ContextualInteraction, ContextualProtagonist
from .interaction import restoreInteraction, deleteInteraction
from .interaction import setInteraction, getInteraction, queryInteraction
from .interaction import joinInteraction, removeFromInteraction
from .interfaces import IAutoResolvingPermission, IPermission
from .interfaces import IPrincipal, IUnauthenticatedPrincipal, IProtagonist
from .interfaces import IProtectedComponent, ISecurityCheck
from .meta import permissions, permission_component
from .principal import Principal, unauthenticated_principal
from .registry import security_registry


def get_principal():
    """Utility method that returns a principal from the current Interaction
    if and only if the interaction contains a single protagonist.
    """
    interaction = queryInteraction()
    if interaction is not None:
        if len(interaction) == 1:
            protagonist = next(iter(interaction))
            return protagonist.principal
    return None
