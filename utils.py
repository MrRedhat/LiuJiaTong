cardDictSI = {
    '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, 'B': 10,
    'J': 11, 'Q': 12, 'K': 13, 'A': 14,
    '2': 15, '0': 16, '1': 17, 'F': 0
}
cardDictIS = {
    3: '3', 4: '4', 5: '5', 6: '6',
    7: '7', 8: '8', 9: '9', 10: 'B',
    11: 'J', 12: 'Q', 13: 'K', 14: 'A',
    15: '2', 16: '0', 17: '1', 0: 'F'
}
def str_to_int(c=''):
    return cardDictSI[c] if c in cardDictSI else -1


def int_to_str(x=-1):
    print("This is x:", x)
    return cardDictIS[x] if x in cardDictIS else '-'


# 返回上一位出牌玩家下标
def last_played(played_cards, tag):
    i = (tag - 1 + 6) % 6
    while i != tag:
        if len(played_cards[i]) != 0:
            return i
        i = (i - 1 + 6) % 6
    return tag
