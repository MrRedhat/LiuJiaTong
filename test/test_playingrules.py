#!/usr/bin/env python
#!coding:utf-8
import pytest
import sys
from ..client.playingrules import *

    
@pytest.mark.parametrize('user_input, user_card, if_first_played, last_played_cards, expect', [
    [[0], [4], True, [], (False, 0)],
    [[0], [4], True, [3], (False, 0)],
    [[4,5,16,17,8], [4,5,6,7,8,9,9,9,9,9,10,13,14,14,14,15,16,17], True, [], (True, 5)],
    [[4,5,16,17,8], [4,5,6,7,8,9,9,9,9,9,10,13,14,14,14,15,16,17], True, [3,4,5,16,17], (True, 5)],
])
def test_if_input_legal(user_input, user_card, if_first_played, last_played_cards, expect):
    assert if_input_legal(user_input, user_card, if_first_played, last_played_cards)==expect
