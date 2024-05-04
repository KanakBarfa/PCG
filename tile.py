import pygame
class Tile:
    def __init__(self, img, edges, i=None):
        self.img = img
        self.edges = edges
        self.up = []
        self.right = []
        self.down = []
        self.left = []

        if i is not None:
            self.index = i

    def analyze(self, tiles):
        for i, tile in enumerate(tiles):
            # Tile 5 can't match itself
            if tile.index == 5 and self.index == 5:
                continue

            # UP
            if self.compare_edge(tile.edges[2], self.edges[0]):
                self.up.append(i)
            # RIGHT
            if self.compare_edge(tile.edges[3], self.edges[1]):
                self.right.append(i)
            # DOWN
            if self.compare_edge(tile.edges[0], self.edges[2]):
                self.down.append(i)
            # LEFT
            if self.compare_edge(tile.edges[1], self.edges[3]):
                self.left.append(i)

    def rotate(self, num):
        # Rotate the tile image
        new_img = pygame.transform.rotate(self.img,90*num)

        # Rotate the edges
        new_edges = [self.edges[(i - num + len(self.edges)) % len(self.edges)] for i in range(len(self.edges))]

        return Tile(new_img, new_edges, self.index)

    @staticmethod
    def compare_edge(a, b):
        return a == b[::-1]
