import pygame
import random
import imageio.v2 as imageio
import os
from tile import Tile
from cell import Cell

# Define constants
DIM = 15
TILE_SIZE = 50
WINDOW_WIDTH = DIM * TILE_SIZE
WINDOW_HEIGHT = DIM * TILE_SIZE

gif_writer = imageio.get_writer("map_generation.gif", mode="I")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def remove_duplicated_tiles(tiles):
    unique_tiles_map = {}
    for tile in tiles:
        key = ','.join(tile.edges)
        unique_tiles_map[key] = tile
    return list(unique_tiles_map.values())

# Define tile images
tile_images = []
path = 'circuit'
for i in range(13):
    tile_images.append(pygame.image.load(f"{path}/{i}.png"))

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Map Generation with WFC")

# Initialize grid
tiles = []
tiles.append(Tile(tile_images[0],['AAA', 'AAA', 'AAA', 'AAA'],0))
tiles.append(Tile(tile_images[1],['BBB', 'BBB', 'BBB', 'BBB'],1))
tiles.append(Tile(tile_images[2],['BBB', 'BCB', 'BBB', 'BBB'],2))
tiles.append(Tile(tile_images[3],['BBB', 'BDB', 'BBB', 'BDB'],3))
tiles.append(Tile(tile_images[4],['ABB', 'BCB', 'BBA', 'AAA'],4))
tiles.append(Tile(tile_images[5],['ABB', 'BBB', 'BBB', 'BBA'],5))
tiles.append(Tile(tile_images[6],['BBB', 'BCB', 'BBB', 'BCB'],6))
tiles.append(Tile(tile_images[7],['BDB', 'BCB', 'BDB', 'BCB'],7))
tiles.append(Tile(tile_images[8],['BDB', 'BBB', 'BCB', 'BBB'],8))
tiles.append(Tile(tile_images[9],['BCB', 'BCB', 'BBB', 'BCB'],9))
tiles.append(Tile(tile_images[10],['BCB', 'BCB', 'BCB', 'BCB'],10))
tiles.append(Tile(tile_images[11],['BCB', 'BCB', 'BBB', 'BBB'],11))
tiles.append(Tile(tile_images[12],['BBB', 'BCB', 'BBB', 'BCB'],12))

# Rotate and remove duplicated tiles
initial_tile_count = len(tiles)
for i in range(initial_tile_count):
    temp_tiles = [tiles[i].rotate(j) for j in range(4)]
    temp_tiles=remove_duplicated_tiles(tiles)
    tiles += [tile for tile in temp_tiles if tile not in tiles]

# Generate adjacency rules based on edges

for tile in tiles:
    tile.analyze(tiles)
    
def start_over():
    # Create cell for each spot on the grid
    grid = [Cell(len(tiles)) for _ in range(DIM * DIM)]
    return grid

def check_valid(arr, valid):
    for i in reversed(range(len(arr))):
        if arr[i] not in valid:
            arr.pop(i)

# Initialize grid
grid = start_over()


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
            if cell.collapsed:
                index = cell.options[0]
                screen.blit(pygame.transform.scale(tile_images[index], (TILE_SIZE, TILE_SIZE)), (i * TILE_SIZE, j * TILE_SIZE))
            else:
                pygame.draw.rect(screen, (51, 51, 51), (i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Pick cell with least entropy
    grid_copy = [cell for cell in grid if not cell.collapsed]

    if not grid_copy:
        pygame.image.save(screen, f"frame_{frame_counter:03d}.png")
        gif_writer.append_data(imageio.imread(f"frame_{frame_counter:03d}.png"))
        frame_counter += 1
        running=False
        break

    grid_copy.sort(key=lambda cell: len(cell.options))
    len_ = len(grid_copy[0].options)
    stop_index = next((i for i, cell in enumerate(grid_copy[1:], start=1) if len(cell.options) > len_), None)
    
    if stop_index is not None:
        grid_copy = grid_copy[:stop_index]

    cell = random.choice(grid_copy)
    cell.collapsed = True
    if len(cell.options)==0:
        grid = start_over()
        continue
    pick = random.choice(cell.options)
    
    
    cell.options = [pick]

    next_grid = []
    for j in range(DIM):
        for i in range(DIM):
            index = i + j * DIM
            if grid[index].collapsed:
                next_grid.append(grid[index])
            else:
                options = list(range(len(tiles)))
                if j > 0:
                    up = grid[i + (j - 1) * DIM]
                    valid_options = sum([tiles[option].down for option in up.options], [])
                    check_valid(options, valid_options)
                if i < DIM - 1:
                    right = grid[i + 1 + j * DIM]
                    valid_options = sum([tiles[option].left for option in right.options], [])
                    check_valid(options, valid_options)
                if j < DIM - 1:
                    down = grid[i + (j + 1) * DIM]
                    valid_options = sum([tiles[option].up for option in down.options], [])
                    check_valid(options, valid_options)
                if i > 0:
                    left = grid[i - 1 + j * DIM]
                    valid_options = sum([tiles[option].right for option in left.options], [])
                    check_valid(options, valid_options)
                
                next_grid.append(Cell(options))
    
    grid = next_grid
    pygame.image.save(screen, f"frame_{frame_counter:03d}.png")
    gif_writer.append_data(imageio.imread(f"frame_{frame_counter:03d}.png"))
    frame_counter += 1
    pygame.display.flip()
gif_writer.close()
for i in range(frame_counter):
    os.remove(f"frame_{i:03d}.png")
pygame.quit()
