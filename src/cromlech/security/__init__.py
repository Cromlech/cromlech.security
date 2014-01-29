# -*- coding: utf-8 -*-

from .registry import security_registry
from .meta import secured_component, permission, security_checker
from .interfaces import IPrincipal, IUnauthenticatedPrincipal, IProtagonist
from .interfaces import ISecuredComponent, ISecurityCheck
from .interfaces import IAutoResolvingPermission, IPermission
from .principal import Principal, unauthenticated_principal
from .components import Protagonist, Interaction
from .interaction import ContextualInteraction, ContextualProtagonist
from .interaction import setInteraction, getInteraction, queryInteraction
from .interaction import restoreInteraction, deleteInteraction
from .decorators import component_protector
from .errors import Unauthorized, Forbidden, MissingSecurityContext


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
