from collections import namedtuple

Card = namedtuple('Card', ['value', 'suit'])


def card_string(played_cards):
    lines = [[] for _ in range(10)]
    for played_card in played_cards:
        card = played_card.card
        player = played_card.player
        # add the individual card on a line by line basis
        lines[0].append('{0}{1}'.format(player.name, ' ' * (11 - len(player.name))))
        lines[1].append('┌─────────┐')
        lines[2].append('│{}        │'.format(card.value))  # use two {} one for char, one for space or char
        lines[3].append('│         │')
        lines[4].append('│         │')
        lines[5].append('│    {}    │'.format(card.suit.name))
        lines[6].append('│         │')
        lines[7].append('│         │')
        lines[8].append('│       {} │'.format(card.value))
        lines[9].append('└─────────┘')
    result = []
    for index, line in enumerate(lines):
        result.append(''.join(lines[index]))
    return '\n'.join(result)
