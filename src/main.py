import random
import time
import pygame
import math
import threading

# Constants
BOMB_VALUE = -2
BOOM_VALUE = -3
UNINITIALIZED_VALUE = -1
CELL_SIZE = 8, 8

screensize = 800,800
grid_size = 8,8
render_scale = (screensize[0]//grid_size[0], screensize[1]//grid_size[1])
refresh_rate = 30
bomb_coords = []
screen = None
loop_running = True
score = 0
won = False
score_limit = 0

def on_gameover():
    print("Game Over")
    
    def stop_loop():
        global loop_running
        loop_running = False
    
    timer = threading.Timer(5, stop_loop)
    timer.start()

class Cell:
    def __init__(self, number: int, border: bool):
        self.number = number
        self.border = border
        self.revealed = False
class Grid:
    def __init__(self, size):
        self.grid_size = size
        self.grid = [[Cell(UNINITIALIZED_VALUE, True) for i in range(size[0])] for j in range(size[1])]
    
    def generate(self, num_of_bombs):
        # Generate bombs
        used_coords = []
        for i in range(num_of_bombs):
            x = random.randint(0, self.grid_size[0]-1)
            y = random.randint(0, self.grid_size[1]-1)
            if (x,y) in used_coords:
                i -= 1
                continue
            self.grid[x][y].number = BOMB_VALUE
            used_coords.append((x,y))
        self.bomb_coords = used_coords

        possible_coords = self.grid_size[0] * self.grid_size[1]
        global score_limit
        score_limit = possible_coords - num_of_bombs
        print("Score limit: ", score_limit) 

            
    
    def __getitem__(self, key):
        return self.grid[key]
    
    def __setitem__(self, key, value):
        self.grid[key] = value

def get_adjacent_bombs(grid: Grid, pos):
    x,y = pos
    bomb_count = 0
    for i in range(-1,2):
        for j in range(-1,2):
            if i == 0 and j == 0:
                continue
            if x+i < 0 or x+i >= grid.grid_size[0] or y+j < 0 or y+j >= grid.grid_size[1]:
                continue
            if grid[x+i][y+j].number == BOMB_VALUE:
                bomb_count += 1
    return bomb_count

def on_cell_click(grid: Grid, pos):
    global score
    x = math.floor(pos[0] / render_scale[0])
    y = math.floor(pos[1] / render_scale[1])
    #print(x,y)
    cell: Cell = grid[x][y]
    cell.revealed = True
    if cell.number == BOMB_VALUE:

        # SET OFF ALL BOMBS
        for x,y in grid.bomb_coords:
            grid[x][y].number = BOOM_VALUE
            grid[x][y].revealed = True
        print("You lose!")
        on_gameover()
    else:
        if cell.number == UNINITIALIZED_VALUE:
            cell.number = get_adjacent_bombs(grid, (x,y))
            score += 1
        if score == score_limit:
            # EXPOSE ALL BOMBS
            for x,y in grid.bomb_coords:
                grid[x][y].revealed = True
            print("You win!")
            global won
            won = True
            on_gameover()
            
    
def get_cell_visual(cell: Cell):
    # Create sprite
    sprite = pygame.sprite.Sprite()
    sprite.image = pygame.Surface(CELL_SIZE)
    sprite.image.fill((255,255,255))

    # Blit images to sprite
    border_image = pygame.image.load(f"./sprites/spriteborder.png")
    sprite.image.blit(border_image, (0,0))
    

    if not cell.revealed:
        #image = pygame.image.load(f"./sprites/spriteunknown.png")
        #sprite.image.blit(image, (1,1))
        pass
    elif cell.number == BOMB_VALUE:
        bomb_image = pygame.image.load(f"./sprites/spritebomb1.png")
        sprite.image.blit(bomb_image, (1,1))
    elif cell.number == BOOM_VALUE:
        boom_image = pygame.image.load(f"./sprites/spritebomb2.png")
        sprite.image.blit(boom_image, (1,1))
    elif cell.number != UNINITIALIZED_VALUE:
        number_image = pygame.image.load(f"./sprites/sprite{cell.number}.png")
        sprite.image.blit(number_image, (1,1))
    else:
        pass

    

    return sprite

def start_window():
    global screen

    print("Refresh rate: ", refresh_rate, "Grid size: ", grid_size, "Screen size: ", screensize,"Render scale: ", render_scale)


    pygame.init()
    screen = pygame.display.set_mode(screensize)
    screen.fill((255, 255, 255))
    pygame.display.set_caption("Minesweeper")

    # Render update
    def render(grid: Grid):
        for x in range(grid.grid_size[0]):
            for y in range(grid.grid_size[1]):
                cell = grid.grid[x][y]
                
                sprite = get_cell_visual(cell)
                scaled_image = pygame.transform.scale(sprite.image, (render_scale[0], render_scale[1]))
                sprite.rect = scaled_image.get_rect()
                sprite.rect.topleft = (x*render_scale[0], y*render_scale[1])
                screen.blit(scaled_image, sprite.rect)
                
                
        
        pygame.display.flip()
               

    grid = Grid(grid_size)
    grid.generate(10)

    global loop_running

    while loop_running:
        time.sleep(1/refresh_rate)
        render(grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                on_cell_click(grid, pos)
        
def main():
    global score
    start_window()
    return score, won

if __name__ == "__main__":
    main()