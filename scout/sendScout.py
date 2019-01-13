from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
import datetime

class PeriodicSenderScout(Agent):
    class InformBehav(PeriodicBehaviour):
        def addBehav(self,nom):
            self.nom = nom
        async def run(self):
            print(f"PeriodicSenderBehaviour running at {datetime.datetime.now().time()}: {self.counter}")
            msg = Message(to="lmworker1@conversejs.org")  # Instantiate the message
            msg.body = "NOPOS"  # Set the message content

            await self.send(msg)
            print("Message sent!")

            if self.counter == 5:
                self.kill()
            self.counter += 1

        async def on_end(self):
            # stop agent from behaviour
            self.agent.stop()

        async def on_start(self):
            self.counter = 0

    def setup(self):
        print(vars(self))
        print(f"PeriodicSenderAgent started at {datetime.datetime.now().time()}")
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=5)
        b = self.InformBehav(period=2, start_at=start_at)
        b.addBehav("xDD")
        self.add_behaviour(b)
