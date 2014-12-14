# -*- coding: utf-8 -*-

from zope.interface import Interface, Attribute, implementer
from zope.interface.common.interfaces import IException, IAttributeError
from zope.schema import Text, TextLine


class ISecurityException(IException):
    pass


class IUnauthorized(ISecurityException):
    pass


class IForbidden(ISecurityException):
    pass


@implementer(IUnauthorized)
class Unauthorized(Exception):
    """Some user wasn't allowed to access a resource.
    """


@implementer(IForbidden)
class Forbidden(Exception):
    """A resource cannot be accessed under any circumstances.
    """


@implementer(ISecurityException)
class MissingSecurityContext(Exception):
    """A security component is missing. The security infrastructure is
    unable to compute anything.
    """

