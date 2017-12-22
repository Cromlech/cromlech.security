# -*- coding: utf-8 -*-

from crom import testing


needs_registry = (
    'test_secure_component.txt',
)


def pytest_runtest_setup(item):
    if item.name in needs_registry:
        testing.setup()


def pytest_runtest_teardown(item):
    if item.name in needs_registry:
        testing.teardown()
