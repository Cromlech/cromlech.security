cromlech.security
=================

``cromlech.security`` provides base security components and utilities to
cook your own security policy.


Protagonist and Interaction
---------------------------

The base of a security policy is to know the `who`.
For this effect, `cromlech.security` proposes three components.

The `Principal` component represents an actor in the application.
A principal is defined by a few attributes : an id, a title and a
description. By default, a principal exists : `unauthenticated_principal`.
It will the one used in every security context until a new one is set.

The `Interaction` component represents a security context in which
one or several principals interact with the application. Interactions
can be nested, to allow a change of security context, for specific
operations (masquarading, admin tasks...).

The `Protagonist` is a conceptual wrapper around a principal, marking it as
belonging to an active interaction.


Permissions
-----------

Permissions are very basic named components.
By default, they are registered in a specific registry :
`cromlech.security.registry.security_registry`.
Out-of-the-box, permissions don't have any specific methods.
They are bricks with which you can secure components.


Securing components
-------------------

See doctests.
