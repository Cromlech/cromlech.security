# -*- coding: utf-8 -*-

from zope.interface import Interface, Attribute, implements
from zope.interface.common.interfaces import IException, IAttributeError
from zope.schema import Text, TextLine


class ISecurityException(IException):
    pass


class IUnauthorized(ISecurityException):
    pass


class IForbidden(ISecurityException):
    pass


class Unauthorized(Exception):
    """Some user wasn't allowed to access a resource.
    """
    implements(IUnauthorized)


class Forbidden(Exception):
    """A resource cannot be accessed under any circumstances.
    """
    implements(IForbidden)


class MissingSecurityContext(Exception):
    """A security component is missing. The security infrastructure is
    unable to compute anything.
    """
    implements(ISecurityException)
