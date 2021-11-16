import pygame
import numpy as np
import random
import math

winSize = (900, 900)
WHITE = (255, 255, 255)
GRAY = (220, 220, 220)
BLACK = (0, 0, 0)
SIZE = 6
CHANCE = 50


class Game:
    def __init__(self, N):
        self.paused = False
        self.mouse_down = False
        N += 1
        self.N = N
        self.grid = np.zeros(N*N, dtype='i').reshape(N, N)
        self.tGrid = np.zeros(N*N, dtype='i').reshape(N, N)
        for i in range(10):
            for j in range(10):
                if random.randint(0, 100) > CHANCE:
                    self.grid[self.N // 2 + i][self.N // 2 + j] = 1
                    self.grid[self.N // 3 + i][self.N // 3 + j] = 1

    def __handle_mouse_down(self):
        if self.mouse_down:
            p = pygame.mouse.get_pos()
            x = p[0] // SIZE
            y = p[1] // SIZE
            self.grid[x][y] = 0 if self.grid[x][y] == 1 else 1

    def main(self, scn):
        pygame.time.delay(0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_down = True
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_down = False

            self.__handle_mouse_down()
            scn.fill(WHITE)
            if not self.paused:
                self.updateGrid()
            self.drawGrid(scn)
            pygame.display.flip()

    def drawGrid(self, scn):
        for i in range(1 + winSize[0] // SIZE):
            for j in range(1 + winSize[1] // SIZE):
                if self.grid[i][j] == 1:
                    pygame.draw.rect(
                        scn, BLACK, (SIZE*i, SIZE*j, SIZE, SIZE), 0)
                else:
                    pygame.draw.rect(
                        scn, GRAY, (SIZE*i, SIZE*j, SIZE-1, SIZE-1), 0)

    def updateGrid(self):
        for i in range(self.N):
            for j in range(self.N):
                cnt = self.live_neighbours(i, j)
                if cnt < 2:
                    self.tGrid[i][j] = 0
                elif cnt == 2:
                    self.tGrid[i][j] = self.grid[i][j]
                elif cnt == 3:
                    self.tGrid[i][j] = 1
                elif cnt > 3:
                    self.tGrid[i][j] = 0
        self.grid = self.tGrid.copy()
        pass

    def live_neighbours(self, i, j):
        s = 0
        for x in [i-1, i, i+1]:
            for y in [j-1, j, j+1]:
                if(x == i and y == j):
                    continue
                if(x != self.N and y != self.N):
                    s += self.grid[x][y]
                elif(x == self.N and y != self.N):
                    s += self.grid[0][y]
                elif(x != self.N and y == self.N):
                    s += self.grid[x][0]
                else:
                    s += self.grid[0][0]
        return s


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(winSize)

    Game(winSize[0] // SIZE).main(screen)
