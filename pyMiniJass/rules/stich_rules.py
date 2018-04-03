def stich_rule(played_cards):
    first_suit = played_cards[0][1].suit
    suit_played_cards = []
    for played_card in played_cards:
        if played_card[1].suit == first_suit:
            suit_played_cards.append(played_card)
    return get_highest(suit_played_cards)


def get_highest(played_cards):
    highest_card = played_cards[0]
    for i in range(1, len(played_cards)):
        if played_cards[i][1].value > highest_card[1].value:
            highest_card = played_cards[i]
    return highest_card


def card_allowed(first_card, hand_cards, chosen_card):
    if chosen_card not in hand_cards:
        return False
    else:
        return True


def allowed_cards(first_card, hand_cards):
    return hand_cards
