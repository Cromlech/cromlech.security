# -*- coding: utf-8 -*-

import cromlech.security
from zope.security.interfaces import IParticipation
from zope.security.management import getInteraction


def test_unauthenticated():
    principal = cromlech.security.unauthenticated_principal
    assert cromlech.security.IUnauthenticatedPrincipal.providedBy(principal)


def test_participation():
    principal = cromlech.security.unauthenticated_principal
    participation = cromlech.security.Participation(principal)
    assert IParticipation.providedBy(participation)


def test_controler():
    principal = cromlech.security.unauthenticated_principal
    with cromlech.security.Interaction(principal) as user:
        assert user == principal
        policy = getInteraction()
        assert len(policy.participations) == 1
        assert policy.participations[0].principal == user
