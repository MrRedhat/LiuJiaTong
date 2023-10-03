from collections import Counter
from enum import Enum
from .Cards import *


# 判断手中牌是否足够出，并返回输入牌的分数
def if_enough_card(user_input: list[int], user_card: list[int]):
    input_num = dict(Counter(user_input))  # 统计每种牌有多少张
    card_num = dict(Counter(user_card))
    for k, v in input_num.items():
        if card_num.get(k, 0) < v:
            return False, 0
    return True, input_num.get(5, 0) * 5 + (input_num.get(10, 0) + input_num.get(13, 0)) * 10


# 判断输入是否合法，若合法，返回重新排列后的输入
def if_input_legal(
    user_input: list[int],
    user_card: list[int],
    if_first_played=False,
    last_played_cards: list[int]=[]
) -> tuple[bool, int]:
    if len(user_input) == 1 and user_input[0] == 0:
        return (False, 0) if if_first_played else (True, 0)  # 第一位玩家不能跳过
    
    for _card in user_input:
        if _card <= 0 or _card > 17: return False, 0  # 非法卡牌

    _if_enough, score = if_enough_card(user_input, user_card)
    if not _if_enough: return False, 0

    _cards = Cards(user_input)
    type_card, key_card = _cards.get_card_type()
    _legal = type_card is not CardType.illegal_type
    if if_first_played:
        return (_legal, score)
    else:
        if not _legal: return False, score
        _last_cards = Cards(last_played_cards)
        last_type_card, last_key_card = _last_cards.get_card_type()

        # 先判断炸弹
        last_if_bomb = last_type_card.value if 1 <= last_type_card.value <= 3 else 0
        _if_bomb = type_card.value if 1 <= type_card.value <= 3 else 0

        if last_if_bomb != 0 and _if_bomb == 0: return False, score     # 上家炸弹
        if last_if_bomb == 0 and _if_bomb != 0: return True, score      # 下家炸弹
        if last_if_bomb != 0 and _if_bomb != 0:                         # 都是炸弹
            if last_if_bomb > _if_bomb: return _cards.card_len > 8, score      # 9张以上比王炸大
            if last_if_bomb < _if_bomb: return _last_cards.card_len < 9, score # 王炸只能炸8张
            # nomal_bomb先比长度再比大小
            if _last_cards.card_len != _cards.card_len:
                return _last_cards.card_len < _cards.card_len, score
            else: return last_key_card < key_card, score
        if type_card is not last_type_card: return False, score # 先看牌型再比Key牌
        return last_key_card < key_card, score
