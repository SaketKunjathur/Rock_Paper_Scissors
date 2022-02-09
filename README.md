# Rock Paper Scissors

## general idea

In this game I have made the basic rock paper scissors game with all the extra screens
like menus etc. and I have also added a save score button which would save the score according
to 2 criterias. The rest of the the game is pretty much the simple rock paper scissors game.

## info. about score management 

2 criterias for saving the score:
* Firstly the game saves the score into a txt file name `score.txt`
* then it checks wether the player has hit a highscore, if yes then it replaces the score
in the file with the player's score

(NOTE: you don't need to create any txt file for the score or highscore. If the program
does not find required txt files it creates a new and then stores the score.
In case you have created one already the program won't show you any error.
If it does then you may check the name of the file).

## tools

Software used for the game dev:
* Sublime Text 3 - __editor__
* Gimp - __art__
* [KataSDK](https://github.com/gaudiatech/katasdk-public) - __python lib__ that allows to run the game in the browser
