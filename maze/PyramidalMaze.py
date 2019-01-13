from array import *
import math
import datetime
from random import randint
class PyramidalMaze:
    def __init__(self,width):
        self.maze = []
        numberWalls = math.floor(width/2 )-2
        posWalls = []
        for i in range (0, numberWalls):
            posWalls.append([])
        for x in range (0,width) :
            oneDim = []
            for y in range (0,width) :
                valueToAdd = 1
                indexWalls = 0;
                for z in range(2,math.ceil(width/2+1),2):
                    if( ((x==z-1 or x == width-z ) and y>=z-1 and y<=width-z) or ((y==z-1 or y == width-z ) and x>=z-1 and x<=width-z)):
                        valueToAdd = 2
                        posWalls[indexWalls].append([x,y])
                    indexWalls+=1
                oneDim.append(valueToAdd)
            self.maze.append(oneDim)
        for i in range (0,len(posWalls)):
            indexDoor = randint(0,len(posWalls[i])-1)
            posDoor = posWalls[i][indexDoor]
            self.maze [posDoor[0]][posDoor[1]] = 3
        print(self.maze)
        

