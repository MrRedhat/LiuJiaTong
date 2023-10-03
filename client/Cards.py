import copy
from enum import Enum
from collections import Counter
'''
3 ~ 15 -> 3 ~ 10 + J Q K A 2
16, 17 -> Joker
关键牌即用于比较俩出牌的大小
'''
# 出牌类型
class CardType(Enum):
    illegal_type = 0
    normal_bomb = 1
    black_joker_bomb = 2
    red_joker_bomb = 3
    straight = 4
    straight_pairs = 5
    straight_triples = 6
    flight = 7
    single = 8
    pair = 9
    triple = 10
    triple_pair = 11


class Cards:
    def __init__(self, cards: list[int]):
        cards.sort(reverse=True) # 逆序排列
        self.cards = cards
        self.card_len = len(cards)
        self.card_type = CardType.illegal_type
        self.key_card = 0
        self.judge_card_type()
    
    def set_type_key(self, card_type: CardType, key_card: int):
        self.card_type = card_type
        self.key_card = key_card
    
    def judge_card_type(self):
        if self.card_type is not CardType.illegal_type: return self.card_type, self.key_card
        self.card_num = dict(Counter(self.cards))  # 统计每种牌有多少张
        self.joker_num = self.card_num.get(16, 0) + self.card_num.get(17, 0)
        self.normal_card_num = dict(Counter(self.cards[self.joker_num:]))
        self.type_num = dict(Counter([v for k, v in self.card_num.items() if k <= 15]))  # 统计除去王牌 相同张数的牌有多少种
        if self.if_bomb(): return self.card_type, self.key_card              # 1 2 3
        if self.if_single(): return self.card_type, self.key_card            # 8
        if self.if_pair(): return self.card_type, self.key_card              # 9
        if self.if_triple(): return self.card_type, self.key_card            # 10
        if self.if_triple_pair(): return self.card_type, self.key_card       # 11
        if self.if_straight(): return self.card_type, self.key_card          # 4
        if self.if_straight_pairs(): return self.card_type, self.key_card    # 5
        if self.if_straight_triples(): return self.card_type, self.key_card  # 6
        if self.if_flight(): return self.card_type, self.key_card            # 7
        self.set_type_key(CardType.illegal_type, 0)
        return self.card_type, self.key_card
    
    def get_card_type(self):
        return self.card_type, self.key_card

    # 判断是否为炸弹
    def if_bomb(self) -> bool:
        if len(self.cards) < 4: return False
        if self.card_num.get(16, 0) == 4: self.set_type_key(CardType.black_joker_bomb, 16)  # 小王炸
        if self.card_num.get(17, 0) == 4: self.set_type_key(CardType.red_joker_bomb, 17)    # 大王炸
        if self.card_type is not CardType.illegal_type: return True  
        # 统计相同张数的牌（除大小王外），判断是否只有 1 or 0 种
        sp_type_num = sum([1 for k in self.card_num.keys() if 3 <= k <= 15])
        if sp_type_num != 1: return False  # 多种牌
        self.set_type_key(CardType.normal_bomb, self.cards[-1])  # 普通炸弹
        return True
    
    # 判断是否为单张
    def if_single(self) -> bool:
        if(len(self.cards) != 1): return False
        self.set_type_key(CardType.single, self.cards[-1])
        return True

    # 判断是否为对子
    def if_pair(self) -> bool:
        if len(self.cards) != 2 or self.joker_num == 0 and self.cards[0] != self.cards[1]: return False
        self.set_type_key(CardType.pair, self.cards[-1])
        return True
    
    # 判断是否为三张
    def if_triple(self):
        if len(self.cards) != 3 or len(self.normal_card_num) > 1: return False  # 除王之外只能有一种牌
        self.set_type_key(CardType.triple, self.cards[-1]); return True

    # 判断是否为三带二，返回（出牌类型，关键牌，转换后牌）
    def if_triple_pair(self):
        if len(self.cards) != 5 or len(self.normal_card_num) != 2: return False  # 牌数不对
        if self.type_num.get(4, 0) == 1: return False
        if self.joker_num == 3: self.set_type_key(CardType.triple_pair, self.cards[3])
        else: self.set_type_key(CardType.triple_pair, self.cards[2])
        return True
    
    # 尝试凑牌
    def try_transform_cards(self, rg: range, try_num: int) -> bool:
        joker_num = self.joker_num
        for i in rg:
            if self.card_num.get(i, 0) > try_num: return False
            if self.card_num.get(i, 0) < try_num: joker_num -= try_num - self.card_num.get(i, 0)
            if joker_num < 0: return False # 大小王不够替换
        return True

    def if_straight(self):
        if len(self.cards) != 5: return False                                # 顺子只能5张
        if self.type_num.get(1, 0) != 5 and self.joker_num == 0: False       # 有重复牌且不是joker
        if self.cards[self.joker_num] - self.cards[-1] + 1 > 5: return False # 除王之外差值不大于5，cards逆序排列

        # 最小牌为J时，需要从A开始尝试倒序替换大小王
        # 其他情况从最小牌开始尝试递增替换大小王
        rg = range(14, 9, -1) if self.cards[-1] > 10 else range(self.cards[-1], self.cards[-1] + 5)
        if self.try_transform_cards(rg, 1):
            self.set_type_key(CardType.straight, max(list(rg))); return True
        return False
    
    def if_straight_pairs(self) -> bool:
        # 至少4张牌，且为偶数
        _len = len(self.cards)
        if _len < 4 or _len > 24 or _len % 2 == 1: return False
        pairs_num = int(_len // 2)
        if self.cards[self.joker_num] - self.cards[-1] + 1 > pairs_num: return False  # 除王之外差值不大于对数

        # 最小牌为J时, 从A开始尝试倒序替换大小王, 其他情况从最小牌开始尝试递增替换大小王
        rg = range(14, 14 - pairs_num, -1) \
            if self.cards[-1] + pairs_num - 1 > 14 else range(self.cards[-1], self.cards[-1] + pairs_num)

        if self.try_transform_cards(rg, 2):
            self.set_type_key(CardType.straight_pairs, max(list(rg))); return True
        else: return False

    def if_straight_triples(self) -> bool:
        # 至少6张牌，且为3的倍数
        _len = len(self.cards)
        if _len < 6 or _len > 36 or _len % 3 != 0: return False

        triples_num = int(_len // 3)
        if self.cards[self.joker_num] - self.cards[-1] + 1 > triples_num: return False  # 除王之外差值不大于连三张数

        rg = range(14, 14 - triples_num, -1) \
            if self.cards[-1] + triples_num - 1 > 14 else range(self.cards[-1], self.cards[-1] + triples_num)

        if self.try_transform_cards(self.card_num, rg, self.joker_num, 3):
            self.set_type_key(CardType.straight_triples, max(list(rg))); return True
        else: return False

    # 尝试将最小牌作为飞机中的三张或对子，返回（能否，剩余王数）
    def try_min_card_type(card_num, rg, joker_num, try_num):
        for i in rg:
            if card_num.get(i, 0) < try_num:
                joker_num -= try_num - card_num.get(i, 0)
            if joker_num < 0:  # 大小王不够替换
                return False, 0
            if i in card_num:
                card_num[i] = max(card_num[i] - try_num, 0)
        return True, joker_num

    def if_flight(self) -> bool:
        # 至少10张牌，且为5的倍数
        _len = len(self.cards)
        if _len < 10 or _len % 5 != 0: return False

        triple_pair_num = int(_len // 5)
        if triple_pair_num > 12: return False

        rg = range(14, 14 - triple_pair_num, -1) \
            if self.cards[-1] + triple_pair_num - 1 > 14 else range(self.cards[-1], self.cards[-1] + triple_pair_num)

        _card_num = copy.deepcopy(self.card_num)
        key_card = 0

        # 尝试将最小牌作为对子
        if_pairs, _joker_num = self.try_min_card_type(_card_num, rg, self.joker_num, 2)
        if if_pairs:
            min_pair_card = 0
            # 找到剩余非王牌中最小牌
            for i in range(self.cards[-1], self.cards[self.joker_num] + 1):
                if _card_num.get(i, 0) > 0:
                    min_pair_card = i
                    break

            # 若没找到，则尝试用王作为所有三张
            if min_pair_card == 0:
                # 王必须数量刚好
                if _joker_num == triple_pair_num * 3:
                    return CardType.flight, 14
            # 其它情况正常凑连三张
            else:
                _rg = range(14, 14 - triple_pair_num, -1) \
                    if min_pair_card + triple_pair_num - 1 > 14 else range(min_pair_card, min_pair_card + triple_pair_num)

                # 凑成功则记录该连三张的最大张作为关键牌
                if self.try_transform_cards(_card_num, _rg, _joker_num, 3):
                    key_card = max(list(_rg))

        _card_num = copy.deepcopy(self.card_num)
        _key_card = 0

        # 尝试将最小牌作为三张
        if_triples, _joker_num = self.try_min_card_type(_card_num, rg, self.joker_num, 3)
        if if_triples:
            # 将凑出的连三张中最大张作为关键牌
            _key_card = max(list(rg))

            min_pair_card = 0
            # 找到剩余非王牌中最小牌
            for i in range(self.cards[-1], self.cards[self.joker_num] + 1):
                if _card_num.get(i, 0) > 0:
                    min_pair_card = i
                    break

            # 若没找到，则尝试用王作为所有对子
            if min_pair_card == 0:
                # 王必须数量刚好
                # 凑失败则清除关键牌
                if _joker_num != triple_pair_num * 2:
                    _key_card = 0
            # 其它情况正常凑连对
            else:
                _rg = range(14, 14 - triple_pair_num, -1) \
                    if min_pair_card + triple_pair_num - 1 > 14 else range(min_pair_card, min_pair_card + triple_pair_num)

                # 凑失败则清除关键牌
                if self.try_transform_cards(_card_num, _rg, _joker_num, 2) is False:
                    _key_card = 0

        # 取两次尝试中较大牌型
        if key_card >= _key_card and key_card != 0:
            self.set_type_key(CardType.flight, key_card); return True
        elif key_card < _key_card:
            self.set_type_key(CardType.flight, _key_card); return True
        else: return False
