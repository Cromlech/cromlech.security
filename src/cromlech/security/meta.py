# -*- coding: utf-8 -*-

from .registry import security_registry
from .interfaces import ISecurityCheck, IPermission, ISecuredComponent
from grokker import Directive, grokker, directive, validator
from crom import name, registry, target
from zope.interface import Interface, classImplements


permission = Directive(
    'permission', 'cromlech', validator=validator.str_validator)

security_checker = Directive(
    'security_checker', 'cromlech')


def base_security_checker(permission):
    def check_against(component, interaction):
        checkers = ISecurityCheck.subscription(component)
        for checker in checkers:
            error = checker(component, permission, interaction)
            if error is not None:
                return error()
        return None
    return check_against


@grokker
@directive(permission)
@directive(security_checker)
def secured_component(scanner, pyname, component, permission,
                      security_checker=base_security_checker):
    component.__checker__ = security_checker(permission)
    classImplements(component, ISecuredComponent)


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
