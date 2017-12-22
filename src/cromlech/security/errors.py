# -*- coding: utf-8 -*-


class SecurityException(Exception):
    pass


class Unauthorized(SecurityException):
    """Some user wasn't allowed to access a resource.
    """


class Forbidden(SecurityException):
    """A resource cannot be accessed under any circumstances.
    """


class MissingSecurityContext(SecurityException):
    """A security component is missing. The security infrastructure is
    unable to compute anything.
    """

