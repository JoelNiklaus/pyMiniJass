from collections import namedtuple

Card = namedtuple('Card', ['value', 'suit'])


def card_string(cards):
    lines = [[] for i in range(9)]
    for index, card in enumerate(cards):
        # add the individual card on a line by line basis
        lines[0].append('┌─────────┐')
        lines[1].append('│{}        │'.format(card.value))  # use two {} one for char, one for space or char
        lines[2].append('│         │')
        lines[3].append('│         │')
        lines[4].append('│    {}    │'.format(card.suit.name))
        lines[5].append('│         │')
        lines[6].append('│         │')
        lines[7].append('│       {} │'.format(card.value))
        lines[8].append('└─────────┘')
    result = []
    for index, line in enumerate(lines):
        result.append(''.join(lines[index]))
    return result
