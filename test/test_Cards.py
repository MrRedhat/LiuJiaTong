#!/usr/bin/env python
#!coding:utf-8
import pytest
import sys
from ..client.Cards import *

@pytest.mark.parametrize('cards, expect', [
    [[3,3,3,3], (CardType.normal_bomb, 3)],
    [[16,16,16,16], (CardType.black_joker_bomb, 16)],
    [[17,17,17,17], (CardType.red_joker_bomb, 17)],
])
def test_bomb(cards, expect):
    new_cards = Cards(cards)
    assert new_cards.get_card_type()==expect

@pytest.mark.parametrize('cards, expect', [
    [[3,3,3], (CardType.triple, 3)],
    [[17,3,3], (CardType.triple, 3)],
    [[17,16,3], (CardType.triple, 3)],
    [[17,17,17], (CardType.triple, 17)],
])
def test_triple(cards, expect):
    new_cards = Cards(cards)
    assert new_cards.get_card_type()==expect

@pytest.mark.parametrize('cards, expect', [
    [[4,4,3,3,3], (CardType.triple_pair, 3)],
    [[4,4,4,3,3], (CardType.triple_pair, 4)],
    [[17,5,3,3,3], (CardType.triple_pair, 3)],
    [[17,5,5,3,3], (CardType.triple_pair, 5)],
    [[17,5,4,3,3], (CardType.illegal_type, 0)],
])
def test_triple_pair(cards, expect):
    new_cards = Cards(cards)
    assert new_cards.get_card_type()==expect


@pytest.mark.parametrize('cards, expect', [
    [[4,4,3,3], (CardType.straight_pairs, 4)],
    [[17,16,4,4,3,3], (CardType.straight_pairs, 5)],
    [[16,14,13,13], (CardType.straight_pairs, 14)],
])
def test_straight_pairs(cards, expect):
    new_cards = Cards(cards)
    assert new_cards.get_card_type()==expect