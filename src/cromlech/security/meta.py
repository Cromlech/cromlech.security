# -*- coding: utf-8 -*-

from .registry import security_registry
from .interfaces import ISecurityCheck, IPermission
from grokker import Directive, grokker, directive, validator
from crom.directives import name, registry
from zope.interface import Interface


permission = Directive('permission', 'cromlech', validator=validator.is_str)
security_checker = Directive('security_checker', 'cromlech')


def base_security_checker(permission):
    def check_against(component, interaction):
        checkers = ISecurityCheck.subscriptions(component)
        for checker in checkers:
            error = checker(component, permission, interaction)
            if error is not None:
                return error()
        return None


@grokker
@directive(permission)
@directive(security_checker)
def secured_component(scanner, pyname, component, permission, security_checker):

    if permission == NO_PERMISSION_REQUIRED:
        permission = None

    component.__checker__ = security_checker(permission)


@grokker
@directive(name)
@directive(target)
@directive(registry)
def permission_component(scanner, pyname, obj, target, name, registry=security_registry):

    assert target.is_or_extends(IPermission)

    def register():
        registry.register(tuple(), target, name, obj)

    scanner.config.action(
        discriminator=('permission', target, name, registry),
        callable=register)
