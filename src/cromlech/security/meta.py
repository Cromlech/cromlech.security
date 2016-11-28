# -*- coding: utf-8 -*-

from .registry import security_registry
from .interfaces import IPermission
from grokker import ArgsDirective, grokker, directive, validator
from crom import name, registry, target
from zope.interface import Interface, classImplements


permissions = ArgsDirective(
    'permissions', 'cromlech', validator=validator.str_validator)


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
