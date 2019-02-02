from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
import json
import datetime
import copy
import math
messageReceived = []

class Scout(Agent):
    def constructor(self, maze, eel):
        self.maze = maze
        self.eel = eel

    class InformBehav(PeriodicBehaviour):
        def init(self, maze, eel, mr):
            self.level = 0
            self.maze = maze  # maze (array 3D width - height - depth (this dimension is when any agents are on the same cell))
            self.id = 4  # 4 is for scout
            self.messageReceived = mr  # messages that we get from listening to others agents
            self.directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
            # Find where our agent is at time 0
            self.searchPosition()
            # Calculation of the direction to not exit the boundaries of the maze
            self.calcDirection()
            # position of the doors relatively to the direction taken
            self.posDoor = []
            self.doorFounded = []
            self.messageDelivered = False
            self.directionsDoors = [[0, 1], [-1, 0], [0, -1], [1, 0]]
            self.eel = eel  # to render the maze in JS
            self.won = False
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

        def searchDoor(self):  # search if there is a door nearby the agent
            if(self.maze.maze[self.position[0] + self.directionsDoors[self.direction][0]][self.position[1] + self.directionsDoors[self.direction][1]][0] == 2):
                # It means there is a door nearby in an adjacent cell
                print("Scout : I've found a door ! ")
                self.posDoor = [self.position[0],self.position[1]]
                self.doorFounded.append("I found a door (" + str(self.position[0]) +","+ str(self.position[1])+")")

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
                    found = True
            # print("DISTANCE : ",distance)
            return distance

        async def run(self):
            print(self.position)
            # Instantiate the message
            if(len(self.messageReceived) > 0): # The door was opened
                if(self.position == self.posDoor):
                    self.level += 1
                    print("SCOUT reached level : ",self.level+1)
                    self.maze.maze[self.position[0]][self.position[1]].remove(self.id)
                    self.position[0] += self.directionsDoors[self.direction][0] * 2
                    self.position[1] += self.directionsDoors[self.direction][1] * 2
                    self.maze.maze[self.position[0]][self.position[1]] = [self.id] + self.maze.maze[self.position[0]][self.position[1]]  # New position updated
                    if(self.level < math.floor(self.maze.width/2)/2):
                        del self.messageReceived[:]
                        self.posDoor = []
                        self.doorFounded = []
                        self.messageDelivered = False
                    else:
                        print("WE WON !")
                        self.agent.stop()
                else:
                    self.calcNewPos()
            msg = Message(to="lmengineer1@conversejs.org")
            # calculates the distance between this agent and a given agent with its id
            if(self.calcDist(0,5) <= 3 and len(self.doorFounded) != 0) :
                msg.body = str(self.doorFounded)
                await self.send(msg)
                self.messageDelivered = True
            # Our agent will move, we will calculate its next position
            if(self.messageDelivered == False): 
                self.calcNewPos()
            # Search door to help the two other agents
                self.searchDoor()
            # send the movement to the JS side
                json_string = json.dumps(self.maze.maze)
                self.eel.updateMaze(json_string)
            if( len (self.messageReceived) == 1 ):
                print(self.messageReceived)
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
                print("Scout, i received: {}".format(msg.body))
                self.mr.append (msg.body)
            else:
                print("Did not received any message after 10 seconds")
                self.kill()

        async def on_end(self):
            self.agent.stop()

    def setup(self):
        print("ReceiverAgent started")
        b = self.RecvBehav()
        b.constructor(messageReceived)
        self.add_behaviour(b)
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=5)
        b = self.InformBehav(period=0.2, start_at=start_at)
        b.init(self.maze, self.eel, messageReceived)
        self.add_behaviour(b)
