def count_stich(played_cards):
    points = 0
    for played_card in played_cards:
        points += played_card.card.value
    return points