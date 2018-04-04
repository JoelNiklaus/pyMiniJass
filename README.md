# pyMiniJass
pyMiniJass is a minified version of the Schieber Jass game

## Game description
The game consists of 16 cards with two types A and B.
Hence there are cards from 1 to 8 of the type A and the same for type B.
The pyMiniJass consists of four players building two teams.
At the beginning every player gets randomly four cards.
Now randomly one player starts and can choose a card.
The next player has to play a card of the same type if he is able to do so.
When every player has played a card the highest card of the same type as the starting card has wins the round
and gets all the cards. (They are stack next to him and are out of the game)
The round winning player is allowed to begin the new round. 
This leads in a total of four rounds.
At the end of the game all cards are summed up with the value of the card.
The the with the most points wins the game.

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
