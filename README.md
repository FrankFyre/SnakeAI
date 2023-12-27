My first ever game was on the Nokia with N95 Snake 3d version being the nostalgic game for me. Hence, I wanted to create something related to it thus resulting in a snake AI game.

## Base Game
The folder called base game contains the base snake game.


![image](https://github.com/FrankFyre/SnakeAI/assets/89239683/996ae1b5-2934-43a5-a60e-4e1636ad745b)



## Deep Q learning 

First, I tried using Deep Q learning. 


The highest score achieved was 63. The program was run multiple times. I stopped it at around 400 games each time. The AI was not able to win the game as it's major problem is that it keeps looping on itself and dying. 

**Looping on itself**
![Loop on itself](https://github.com/FrankFyre/SnakeAI/assets/89239683/70428588-c2ed-457c-a705-c087ad344790)
![snkae1](https://github.com/FrankFyre/SnakeAI/assets/89239683/09a3596e-b435-4b4d-85e5-52ca23752c1c)


**Graph**

![1maxg](https://github.com/FrankFyre/SnakeAI/assets/89239683/725b6a88-1e34-40cb-8071-8ed33fe23f46)


## Hamilotonian Cycle 


John Tapsell created an AI that was run on the Nokia phone using a Hamiltonian cycle. [Website]([https://pages.github.com/](https://johnflux.com/2015/05/02/nokia-6110-part-3-algorithms/)https://johnflux.com/2015/05/02/nokia-6110-part-3-algorithms/).

Similar to his method, I used Prim's algorithm to  generate random a maze and then create a Hamiltonian cycle. I modified this into the base game which is much more difficult. However, as seen below it eventually worked and the snake AI was able to complete the game.


200x200 screen size  - 50 Block Size
https://github.com/FrankFyre/SnakeAI/assets/89239683/94533e13-7bee-46da-a416-f4e7a81f3b21

600x600 screen size  - 30 Block Size


https://github.com/FrankFyre/SnakeAI/assets/89239683/0af948cb-2951-4ae8-a26e-3b48bdf1ab70

## Ongoing works

Currently, there I cannot figure out how to skip parts of the cycle to speed up the winning of the game. The biggest error that I am trying to fix is that the snake goes off the map and crashes when performing a skip 





###References and credits 
[Base snake game tutorial](https://www.youtube.com/watch?v=L8ypSXwyBds&ab_channel=freeCodeCamp.org)
[Coding Hamiltonian cycle](https://github.com/illayyy/snake_ai)


