# -*- coding: utf-8 -*-

import pytest
from cromlech.security import Protagonist, Principal, ContextualInteraction
from cromlech.security import IUnauthenticatedPrincipal, IProtagonist
from cromlech.security import unauthenticated_principal
from cromlech.security.interaction import getInteraction, endInteraction


def test_unauthenticated():
    principal = unauthenticated_principal
    assert IUnauthenticatedPrincipal.providedBy(principal)


def test_protagonist():
    principal = unauthenticated_principal
    protagonist = Protagonist(principal)
    assert IProtagonist.providedBy(protagonist)


def test_controler():
    principal = unauthenticated_principal
    with ContextualInteraction(principal) as ci:
        interaction = getInteraction()
        assert ci is interaction
        assert len(interaction) == 1
        assert interaction.principals == set([principal])


def test_nested_interaction():
    anon = unauthenticated_principal
    john = Principal('John')
    anke = Principal('Anke')
    paul = Principal('Paul')

    with ContextualInteraction():
        interaction = getInteraction()
        assert interaction.principals == set([anon])

        with ContextualInteraction(john):
            interaction = getInteraction()
            assert interaction.principals == set([john])

            with ContextualInteraction(john, anke):
                interaction = getInteraction()
                assert interaction.principals == set([john, anke])

                with ContextualInteraction(paul):
                    interaction = getInteraction()
                    assert interaction.principals == set([paul])

                interaction = getInteraction()
                assert interaction.principals == set([john, anke])

            interaction = getInteraction()
            assert interaction.principals == set([john])

        interaction = getInteraction()
        assert interaction.principals == set([anon])


def test_aborted_interaction():
    anon = unauthenticated_principal
    john = Principal('John')
    anke = Principal('Anke')
    paul = Principal('Paul')

    with pytest.raises(AssertionError) as e:
        with ContextualInteraction():
            with ContextualInteraction(john):
                endInteraction()

    assert str(e.value) == (
        'Security context has changed during the `Interaction`')
