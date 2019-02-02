from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template
import json
import datetime
import copy
messageReceived = []
import re
from ast import literal_eval
class Worker(Agent):
    def constructor(self, maze, eel):
        self.maze = maze
        self.eel = eel

    class InformBehav(PeriodicBehaviour):
        def init(self, maze, eel, mr):
            self.level = 0
            self.maze = maze  # maze (array 3D width - height - depth (this dimension is when any agents are on the same cell))
            self.id = 6  # 4 is for the worker
            self.messageReceived = mr  # messages that we get from listening to others agents
            self.directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
            self.posDoor = (-1, -1)
            # Find where our agent is at time 0
            self.searchPosition()
            # Calculation of the direction to not exit the boundaries of the maze
            self.calcDirection();
            # position of the doors relatively to the direction taken
            self.directionsDoors = [[0, 1], [-1, 0], [0, -1], [1, 0]]
            self.talkedScout = False
            self.talkedEngineer = False
            self.opened = False
            self.eel = eel  # to render the maze in JS

        def calcNewPos(self):
            # see if we change wheter the position or not
            if(self.position[0] + self.directions[self.direction][0] >= self.maze.width - self.level * 2 or self.position[0] + self.directions[self.direction][0] < self.level*2 or self.position[1] + self.directions[self.direction][1] < self.level*2 or self.position[1] + self.directions[self.direction][1] >= self.maze.width - self.level * 2):
                if(self.direction == 3):  # 4 directions possible that loop
                    self.direction = 0
                else:
                    self.direction = self.direction + 1  # move forward
            try:
                self.maze.maze[self.position[0]][self.position[1]].remove(self.id)  # behind become an empty cell
            except ValueError:
                print("np")  # do nothing
            # update of the position
            self.position[0] += self.directions[self.direction][0]
            self.position[1] += self.directions[self.direction][1]
            self.maze.maze[self.position[0]][self.position[1]] = [self.id] + self.maze.maze[self.position[0]][self.position[1]]  # New position updated
        
        def calcDirection(self):
            width = self.maze.width
            level = self.level
            if(self.position[0] == level*2 and self.position[1] == level*2 ):
                self.direction = 0
            elif(self.position[0] == width - 1 - level*2  and self.position[1] == level*2 ): 
                self.direction = 1
            elif(self.position[0] == width - 1 - level*2 and self.position[1] == width - 1 - level*2): 
                self.direction = 2
            elif(self.position[0] == level*2 and self.position[1] == width - 1 - level*2): 
                self.direction = 3
            elif(self.position[1] == level*2): # in function of the initial position, we give a direction to our agent
                self.direction = 3 # goes up, cause 
            elif(self.position[1] == width - 1 - level*2):
                self.direction = 1
            elif(self.position[0] == level*2):
                self.direction = 0
            elif(self.position[0] == width - 1 - level*2):
                self.direction = 1
            else:
                self.direction = 2

        def searchPosition(self):
            width = self.maze.width
            for i in range(0, width):  # we search our agent in the labyrinth
                for j in range(0, width):
                    if(self.maze.maze[i][j][0] == self.id):
                        self.position = [i, j]

        def calcDist(self, level, idAgent): # it calculates the distance between the agent and the others to   
            found = False
            level = self.level
            distance = -1
            direction = copy.deepcopy(self.direction)
            position = copy.deepcopy(self.position)
            while(found == False ):
                if(position[0] + self.directions[direction][0] >= self.maze.width - level * 2 or position[0] + self.directions[direction][0] < level * 2 or position[1] + self.directions[direction][1] < level * 2 or position[1] + self.directions[direction][1] >= self.maze.width - level * 2 ):
                    if(direction == 3): # 4 directions possible that loop
                        direction = 0
                    else:
                        direction += 1 # move forward
                position[0] += self.directions[direction][0] # update of the position
                position[1] += self.directions[direction][1]
                try: # verify if the agent is in the array of the maze
                    index = self.maze.maze[position[0]][position[1]].index(idAgent)
                except ValueError:
                    index = -1
                if(index != -1) :
                    found = True
                distance += 1
                if(distance > self.maze.width * 4):
                    found = False
            # print("DISTANCE : ",distance)
            return distance

        async def run(self):
            # Instantiate the message
            msg = Message(to="lmengineer1@conversejs.org")
            # send the movement to the JS side
            json_string = json.dumps(self.maze.maze)
            self.eel.updateMaze(json_string)
            if( len (self.messageReceived) > 0 ):
                self.messageReceived[0]
                res = re.search('\(\S+\)',self.messageReceived[0])
                self.posDoor = res.group(0)
            if(self.posDoor[0] != -1):
                if(self.opened == False):
                    pos = literal_eval(self.posDoor)
                    if(pos[0] == self.position[0] and pos[1] == self.position[1]):
                        print("IM OPENING THE DOOR !")
                        self.opened = True
                        self.maze.maze[pos[0] + self.directionsDoors[self.direction][0]][pos[1]+ self.directionsDoors[self.direction][1]] = 0 
                    else:
                        self.calcNewPos()
                else: # From there, the door is open
                    self.calcNewPos()
                    pos = literal_eval(self.posDoor)
                    if(self.position[0] == pos[0] and self.position[1] == pos[1]):
                        self.level += 1
                        print("WORKER achieved level ",self.level)
                        del self.messageReceived[:]
                        self.maze.maze[self.position[0]][self.position[1]].remove(self.id)
                        self.position[0] += self.directionsDoors[self.direction][0] * 2
                        self.position[1] += self.directionsDoors[self.direction][1] * 2
                        self.maze.maze[self.position[0]][self.position[1]] = [self.id] + self.maze.maze[self.position[0]][self.position[1]]  # New position updated
                        self.posDoor = (-1, -1)
                        self.talkedScout = False
                        self.talkedEngineer = False
                        self.opened = False
                    else:
                        if(self.talkedScout == False and self.calcDist(0,4) <= 3) :
                            self.talkedScout = True
                            msg = Message(to="lmscout1@conversejs.org")
                            msg.body = "DOOR OPENED !"
                            await self.send(msg)
                        if(self.talkedEngineer == False and self.calcDist(0,5) <= 3) :
                            self.talkedEngineer = True
                            msg = Message(to="lmengineer1@conversejs.org")
                            msg.body = "DOOR OPENED !"
                            await self.send(msg)
            # self.kill()

        async def on_end(self):
            # stop agent from behaviour
            self.agent.stop()

        async def on_start(self):
            self.counter = 0

    class RecvBehav(CyclicBehaviour):
        def constructor(self, mr):
            self.mr = mr
        async def run(self):
            print("RecvBehav running")
            msg = await self.receive(timeout=1000)  # wait for a message for 1 seconds
            if msg:
                print("I'm the slave and that's what I received {}".format(msg.body))
                self.mr.append (msg.body)
            else:
                print("Did not received any message after 10 seconds")
                self.kill()

        async def on_end(self):
            self.agent.stop()

    def setup(self):
        print("Worker is starting")
        b1 = self.RecvBehav()
        b1.constructor(messageReceived)
        self.add_behaviour(b1)
        start_at = datetime.datetime.now() 
        b2 = self.InformBehav(period=0.2, start_at=start_at)
        b2.init(self.maze, self.eel, messageReceived)
        self.add_behaviour(b2)
        