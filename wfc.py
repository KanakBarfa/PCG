import pygame
import random
import imageio.v2 as imageio
import os


# Define constants
DIM = 15
TILE_SIZE = 50
WINDOW_WIDTH = DIM * TILE_SIZE
WINDOW_HEIGHT = DIM * TILE_SIZE

# Define tile constants
BLANK = 0
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4
gif_writer = imageio.get_writer("map_generation.gif", mode="I")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Define tile images
TILE_IMAGES = {
    BLANK: pygame.image.load("demo_image/blank.png"),
    UP: pygame.image.load("demo_image/up.png"),
    RIGHT: pygame.image.load("demo_image/right.png"),
    DOWN: pygame.image.load("demo_image/down.png"),
    LEFT: pygame.image.load("demo_image/left.png"),
}

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Map Generation with WFC")

# Initialize grid
grid = [{"collapsed": False, "options": [BLANK, UP, RIGHT, DOWN, LEFT]} for _ in range(DIM * DIM)]

rules = [
	[
		[BLANK, UP],
		[BLANK, RIGHT],
		[BLANK, DOWN],
		[BLANK, LEFT],
	],
	[
		[RIGHT, LEFT, DOWN],
		[LEFT, UP, DOWN],
		[BLANK, DOWN],
		[RIGHT, UP, DOWN],
	],
	[
		[RIGHT, LEFT, DOWN],
		[LEFT, UP, DOWN],
		[RIGHT, LEFT, UP],
		[BLANK, LEFT],
	],
	[
		[BLANK, UP],
		[LEFT, UP, DOWN],
		[RIGHT, LEFT, UP],
		[RIGHT, UP, DOWN],
	],
	[
		[RIGHT, LEFT, DOWN],
		[BLANK, RIGHT],
		[RIGHT, LEFT, UP],
		[UP, DOWN, RIGHT],
	],
]


running = True
frame_counter=0
while running:
    screen.fill(BLACK)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Draw grid
    for j in range(DIM):
        for i in range(DIM):
            cell = grid[i + j * DIM]
            if cell["collapsed"]:
                tile_index = cell["options"][0]
                screen.blit(TILE_IMAGES[tile_index], (i * TILE_SIZE, j * TILE_SIZE))
            else:
                pygame.draw.rect(screen, BLACK, (i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    
    # Pick cell with least entropy
    grid_copy = [cell for cell in grid if not cell["collapsed"]]

    if not grid_copy:       # Genration completed
        pygame.image.save(screen, f"frame_{frame_counter:03d}.png")
        gif_writer.append_data(imageio.imread(f"frame_{frame_counter:03d}.png"))
        frame_counter += 1
        running=False
        break
    
    # Sort on the basis of entropy
    grid_copy.sort(key=lambda cell: len(cell["options"]))
    
    stop_index = next((i for i, cell in enumerate(grid_copy[1:], start=1) if len(cell["options"]) > len(grid_copy[0]["options"])), None)
    if stop_index is not None:
        grid_copy = grid_copy[:stop_index]
    
    cell = random.choice(grid_copy)
    cell["collapsed"] = True

    if len(cell["options"])==0: # If we are stuck, need to restart
        grid = [{"collapsed": False, "options": [BLANK, UP, RIGHT, DOWN, LEFT]} for _ in range(DIM * DIM)]
        continue

    pick = random.choice(cell["options"])
    cell["options"] = [pick]

    # Update next grid
    next_grid = []
    for j in range(DIM):
        for i in range(DIM):
            index = i + j * DIM
            if grid[index]["collapsed"]:
                next_grid.append(grid[index])
            else:
                options = set([BLANK, UP, RIGHT, DOWN, LEFT])
                # Look up
                if j > 0:
                    up = grid[i + (j - 1) * DIM]
                    valid_options = []
                    for option in up["options"]:
                        valid_options.extend(rules[option][2])
                    options = options&set(valid_options)
                # Look right
                if i < DIM - 1:
                    right = grid[i + 1 + j * DIM]
                    valid_options = []
                    for option in right["options"]:
                        valid_options.extend(rules[option][3])
                    options = options&set(valid_options)
                # Look down
                if j < DIM - 1:
                    down = grid[i + (j + 1) * DIM]
                    valid_options = []
                    for option in down["options"]:
                        valid_options.extend(rules[option][0])
                    options = options&set(valid_options)
                # Look left
                if i > 0:
                    left = grid[i - 1 + j * DIM]
                    valid_options = []
                    for option in left["options"]:
                        valid_options.extend(rules[option][1])
                    options = options&set(valid_options)
                
                # Updating accordingly
                next_grid.append({"options": list(options), "collapsed": False})

    grid = next_grid
    pygame.display.flip()
    pygame.image.save(screen, f"frame_{frame_counter:03d}.png")
    gif_writer.append_data(imageio.imread(f"frame_{frame_counter:03d}.png"))
    frame_counter += 1

gif_writer.close()
for i in range(frame_counter):
    os.remove(f"frame_{i:03d}.png")
pygame.quit()
