# -*- coding: utf-8 -*-

from .registry import security_registry
from .interfaces import IPermission
from grokker import ArgsDirective, grokker, directive, GrokkerValidationError
from crom import name, registry, target
from zope.interface import Interface, classImplements
from zope.interface.interfaces import IInterface

import sys
if sys.version > '3':
    unicode = str


def permission_validator(directive_name, value):
    if not isinstance(value, (unicode, str, bytes)):
        if not IPermission.providedBy(value):
            raise GrokkerValidationError(
                "The '%s' directive can only be called with a "
                "str or IPermission argument." % directive_name)


permissions = ArgsDirective(
    'permissions', 'cromlech', validator=permission_validator)


@grokker
@directive(name)
@directive(target)
@directive(registry)
def permission_component(scanner, pyname, obj, target=IPermission,
                         name=None, registry=security_registry):

    if name is None:
        name = obj.__name__.__lower__

    assert target.is_or_extends(IPermission)

    def register():
        registry.register(tuple(), target, name, obj)

    scanner.config.action(
        discriminator=('permission', target, name, registry),
        callable=register)
