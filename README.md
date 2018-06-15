# pyMiniJass
pyMiniJass is a minified version of the Schieber Jass game

## Game description

### Structure
The pyMiniJass is structured as the follows:
 - item Two types of cards, named as A and B
 - item 8 cards per type, resulting in a total of 16
 - item Four players, two of them building a team
 - item A game has four rounds
 - item The highest card with the same type of the starting card wins the round

### Gameplay
First the four players have to build two teams of two members each.
In the perspective of every player the order of card choosing is defined as the following.
If you start the round the next player is your first opponent, after that your teammate has to choose and finally your second opponent play the last card of the round.
At the beginning of the game every player gets randomly four cards.
After the card dealing phase a random player starts to choose a card.
Now each player after another has to choose a card of his own ones.
If available, the card chosen card has to be of the same type as the first of the round.
When every player has played a card the highest card of the same type as the starting card wins the round.
The team of the winning player gets as many points as the values of the cards have.
The next round starts with the winner of the last one.
This procedure is repeated until no cards are left, leading to a total of four rounds.
At the end of the game the team with the most points wins.

## CLI
The game provides a simple CLI to play against various players.

```
Table:

Tick       Track      RL1        
┌─────────┐┌─────────┐┌─────────┐
│3        ││1        ││6        │
│         ││         ││         │
│         ││         ││         │
│    B    ││    A    ││    B    │
│         ││         ││         │
│         ││         ││         │
│       3 ││       1 ││       6 │
└─────────┘└─────────┘└─────────┘

Hand cards: 

0          1          2          3          
┌─────────┐┌─────────┐┌─────────┐┌─────────┐
│8        ││6        ││7        ││8        │
│         ││         ││         ││         │
│         ││         ││         ││         │
│    A    ││    A    ││    A    ││    B    │
│         ││         ││         ││         │
│         ││         ││         ││         │
│       8 ││       6 ││       7 ││       8 │
└─────────┘└─────────┘└─────────┘└─────────┘
Please chose the card by the number from 0 to 3: 
3
```
