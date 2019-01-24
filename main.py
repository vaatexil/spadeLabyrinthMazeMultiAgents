# Declaration of all the sender and receiver classes from scouts, workers and engineers
import time
import _thread
from scout.scout import ReceiverScout
from scout.scout import PeriodicSenderScout
from engineer.engineer import ReceiverEngineer
from engineer.engineer import PeriodicSenderEngineer
from worker.worker import ReceiverWorker
from worker.worker import PeriodicSenderWorker
from maze.PyramidalMaze import PyramidalMaze
import eel

eel.init('web')

@eel.expose                         # Expose this function to Javascript
def say_hello_py(x):
    print('Hello from %s' % x)

# say_hello_py('Python World!')
# eel.updateMaze('Python World!')   # Call a Javascript function

def webServer():
    eel.start('main.html', block=False)           # Start (this blocks and enters loop)
    while True:
        eel.sleep(1.0)                  # Use eel.sleep(), not time.sleep()

def receivers():
    receiverEngineer = ReceiverEngineer("lmengineer1@conversejs.org","woweygiowa96")
    receiverEngineer.start()
    receiverScout = ReceiverScout("lmscout1@conversejs.org", "woweygiowa96")
    receiverScout.start()
    receiverWorker = ReceiverWorker("lmworker1@conversejs.org","woweygiowa96")
    receiverWorker.start()

try:
    print("Starting webServer...")
    _thread.start_new_thread( webServer,() ) # launch the server in parallel
    _thread.start_new_thread( receivers, ()) # launch the receiver in parallel with the senders
    print("webServer started !")

except:
   print ("Error: unable to start thread")

if __name__ == "__main__":
    # we create our maze
    maze = PyramidalMaze(9) 

    # We create our senders
    senderScout = PeriodicSenderScout("lmscout1@conversejs.org", "woweygiowa96")
    senderEngineer = PeriodicSenderEngineer("lmengineer1@conversejs.org","woweygiowa96")
    # senderWorker = PeriodicSenderWorker("lmengineer1@conversejs.org","woweygiowa96")
   
    # we launch our senders
    senderScout.constructor(maze,eel)
    senderScout.start()

    # senderEngineer.constructor(maze,eel)
    # senderEngineer.start()

    # senderWorker.constructor(maze,eel)
    # senderWorker.start()
