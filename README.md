# About #
Before this project, I had made two pygame projects and decided that Minesweeper was a good next one. 
This is a first iteration that is function but I can definitely clean up the current code so that's where I'll likely go with any further development alongside maybe other features like a scoreboard, similar to my snake game one.

# Sprite #
This is the first pygame project where I use sprites.
I went with a cell approach to handling each block. Each block was a cell and each cell was an 8x8 pixel block. The border of block is an 8x8 sprite that marks the perimeter of the cell. The inner 6x6 section is used to house the number sprites and bomb sprites so 6x6 sprites were used to actually represent block contents.

# Dependencies #
Pygame
