from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
import json
import datetime
import copy
messageReceived = []


class PeriodicSenderScout(Agent):
    def constructor(self, maze, eel):
        self.maze = maze
        self.eel = eel

    class InformBehav(PeriodicBehaviour):
        def init(self, maze, eel, mr):
            self.maze = maze  # maze (array 3D width - height - depth (this dimension is when any agents are on the same cell))
            self.id = 4  # 4 is for scout
            self.messageReceived = mr  # messages that we get from listening to others agents
            self.directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
            # Calculation of the direction to not exit the boundaries of the maze
            self.calcDirection();
            # Find where our agent is at time 0
            self.searchPosition()
            # position of the doors relatively to the direction taken
            self.directionsDoors = [[0, 1], [-1, 0], [0, -1], [1, 0]]

            self.eel = eel  # to render the maze in JS

        def calcNewPos(self):
            # see if we change wheter the position or not
            if(self.position[0] + self.directions[self.direction][0] >= self.maze.width or self.position[0] + self.directions[self.direction][0] < 0 or self.position[1] + self.directions[self.direction][1] < 0 or self.position[1] + self.directions[self.direction][1] >= self.maze.width):
                if(self.direction == 3):  # 4 directions possible that loop
                    self.direction = 0
                else:
                    self.direction = self.direction + 1  # move forward
            self.maze.maze[self.position[0]][self.position[1]].remove(
                self.id)  # behind become an empty cell
            # update of the position
            self.position[0] += self.directions[self.direction][0]
            self.position[1] += self.directions[self.direction][1]
            self.maze.maze[self.position[0]][self.position[1]] = [
                self.id] + self.maze.maze[self.position[0]][self.position[1]]  # New position updated

        def searchDoor(self):  # search if there is a door nearby the agent
            if(self.maze.maze[self.position[0] + self.directionsDoors[self.direction][0]][self.position[1] + self.directionsDoors[self.direction][1]][0] == 2):
                # It means there is a door nearby in an adjacent cell
                return (self.position[0] + self.directionsDoors[self.direction][0], self.position[1] + self.directionsDoors[self.direction][1])
            return 0

        def calcDirection(self):
            width = self.maze.width
            if(self.position[0] == 0 and self.position[1] == 0):
                self.direction = 0
            elif(self.position[0] == width - 1  and self.position[1] == 0): 
                self.direction = 1
            elif(self.position[0] == width - 1 and self.position[1] == width - 1): 
                self.direction = 2
            elif(self.position[0] == 0 and self.position[1] == width - 1): 
                self.direction = 3
            elif(self.position[0] == 0 or self.position[0] == width -1): # in function of the initial position, we give a direction to our agent
                self.direction = 0
            else:
                self.direction = 1
        def searchPosition(self):
            width = self.maze.width
            for i in range(0, width):  # we search our agent in the labyrinth
                for j in range(0, width):
                    if(maze.maze[i][j][0] == self.id):
                        self.position = [i, j]
        def calcDist(self, level, idAgent): # it calculates the distance between the agent and the others to   
            found = False
            distance = -1
            direction = copy.deepcopy(self.direction)
            position = copy.deepcopy(self.position)
            while(found == False):
                if(position[0] + self.directions[direction][0] >= self.maze.width or position[0] + self.directions[direction][0] < 0 or position[1] + self.directions[direction][1] < 0 or position[1] + self.directions[direction][1] >= self.maze.width ):
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
            print("DISTANCE : ",distance)
            return distance

        async def run(self):
            # Instantiate the message
            msg = Message(to="lmworker1@conversejs.org")
            # calculates the distance between this agent and a given agent with its id
            if(self.calcDist(0,5) <= 3):
                print("SENDING TO THE AGENT")
            # Our agent will move, we will calculate its next position 
            self.calcNewPos()
            # Search door to help the two other agens
            posDoor = self.searchDoor()
            if(posDoor != 0): # it means the scout discover the door
                # Set the message content
                msg.body = "There is a door here : "+str(posDoor)
                await self.send(msg)
                print("Message sent!")
            # send the movement to the JS side
            json_string = json.dumps(self.maze.maze)
            self.eel.updateMaze(json_string)
            if( len (self.messageReceived) > 0 ):
                print(self.messageReceived)
            # self.kill()

        async def on_end(self):
            # stop agent from behaviour
            self.agent.stop()

        async def on_start(self):
            self.counter = 0

    def setup(self):
        print(
            f"PeriodicSenderAgent started at {datetime.datetime.now().time()}")
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=5)
        b = self.InformBehav(period=2, start_at=start_at)
        b.init(self.maze, self.eel, messageReceived)
        self.add_behaviour(b)


class ReceiverScout(Agent):
    class RecvBehav(CyclicBehaviour):
        def constructor(self, mr):
            self.mr = mr
        async def run(self):
            print("RecvBehav running")
            msg = await self.receive(timeout=1000)  # wait for a message for 1 seconds
            if msg:
                print("Message received with content: {}".format(msg.body))
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
