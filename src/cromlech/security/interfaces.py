# -*- coding: utf-8 -*-

# Currently it includes rough forking of zope.security

from zope.interface import Interface, Attribute
from zope.schema import TextLine, Text


class IProtectedComponent(Interface):

    def __check_security__(interaction):
        """Returns:
        - None if the access is allowed.
        - An instance of Unauthorized if the interaction contains
          only unauthenticated users.
        - An instance of Forbidden if the interaction contains
          authenticated users.
        """


class ISecurityCheck(Interface):
    """A security check.
    """
    def __call__(obj, interaction):
        """Checks the security on an interaction.
        Returns:
        - None if the access is allowed.
        - `Unauthorized` if the interaction contains only unauthenticated users.
        - `Forbidden` if the interaction contains authenticated users.
        """


class IPermission(Interface):
    """A permission object."""

    id = TextLine(
        title=u"Id",
        description=u"Id as which this permission will be known and used.",
        readonly=True,
        required=True)

    title = TextLine(
        title=u"Title",
        description=u"Provides a title for the permission.",
        required=True)

    description = Text(
        title=u"Description",
        description=u"Provides a description for the permission.",
        required=False)


class IAutoResolvingPermission(IPermission):

    def __call__(obj, interaction):
        """Checks the interaction against itself on an object.
        Returns:
        - None if the access is allowed.
        - `Unauthorized` if the interaction contains only unauthenticated users.
        - `Forbidden` if the interaction contains authenticated users.
        """


class IPrincipal(Interface):
    """Principals are security artifacts that execute actions in a security
    environment.

    The most common examples of principals include user and group objects.

    It is likely that IPrincipal objects will have associated views
    used to list principals in management interfaces. For example, a
    system in which other meta-data are provided for principals might
    extend IPrincipal and register a view for the extended interface
    that displays the extended information. We'll probably want to
    define a standard view name (e.g.  'inline_summary') for this
    purpose.
    """

    id = TextLine(
        title=u"Id",
        description=u"The unique identification of the principal.",
        required=True,
        readonly=True)

    title = TextLine(
        title=u"Title",
        description=u"The title of the principal.",
        required=False)

    description = Text(
        title=u"Description",
        description=u"A detailed description of the principal.",
        required=False)


class IGroup(IPrincipal):
    """Group of principals
    """


class IUnauthenticatedPrincipal(IPrincipal):
    pass


class IInteraction(Interface):
    """A representation of an interaction between some actors and the system.
    """
    previous = Attribute('Previous interaction')

    def add(protagonist):
        """Add a protagonist.
        """

    def remove(protagonist):
        """Remove a protagonist.
        """

    def __iter__():
        """Iterable of protagonists.
        """

    def __len__():
        """Number of protagonists involved in the interaction.
        """


class IProtagonist(Interface):

    interaction = Attribute("The interaction")
    principal = Attribute("The authenticated principal")
