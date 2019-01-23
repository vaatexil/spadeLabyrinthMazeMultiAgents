from array import *
import math
import datetime
import random
from random import randint

class PyramidalMaze:
    def __init__(self, width):
        self.maze = []
        self.width = width
        self.classes = ["none","walls","doors","treasure","scout","slave", "engi"]
        numberWalls = math.floor(width/2)-2
        posWalls = []
        for i in range(0, numberWalls):
            posWalls.append([])
        for x in range(0, width):
            oneDim = []
            for y in range(0, width):
                valueToAdd = 0
                indexWalls = 0
                for z in range(2, math.ceil(width/2+1), 2):
                    if(((x == z-1 or x == width-z) and y >= z-1 and y <= width-z) or ((y == z-1 or y == width-z) and x >= z-1 and x <= width-z)):
                        valueToAdd = 1
                        if(not ((x == z-1 and y == z - 1) or (x == z-1 and y == width - z) or (x == width - z and y == z - 1) or (x == width - z and y == width - z))):
                            posWalls[indexWalls].append([x, y])
                    indexWalls += 1
                oneDim.append([valueToAdd])
            self.maze.append(oneDim)
        for i in range(0, len(posWalls)):
            indexDoor = randint(0, len(posWalls[i])-1)
            posDoor = posWalls[i][indexDoor]
            self.maze[posDoor[0]][posDoor[1]] = 2
        self.maze[math.floor(width/2)][math.floor(width/2)] = 3  # treasure
        posAgents = [4, 5, 6]
        random.shuffle(posAgents)
        self.maze[randint(1,width -2)][0] = [posAgents[0]]  # we randomly put agents in our maze
        self.maze[width - 1][randint(1,width -2)] = [posAgents[1]]
        self.maze[randint(1,width -2)][width - 1] = [posAgents[2]]
        print(self.maze)
