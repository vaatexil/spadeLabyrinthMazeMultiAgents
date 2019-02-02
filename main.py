# Declaration of all the sender and receiver classes from scouts, workers and engineers
import time
import _thread
from scout.scout import Scout
from engineer.engineer import Engineer
from worker.worker import Worker
from maze.PyramidalMaze import PyramidalMaze
import eel

eel.init('web')

@eel.expose                         # Expose this function to Javascript
def say_hello_py(x):
    print('Hello from %s' % x)

# say_hello_py('Python World!')
# we create our maze
width = 13
eel.initJs(width)   # Call a Javascript function

def webServer():
    eel.start('main.html', block=False)           # Start (this blocks and enters loop)
    while True:
        eel.sleep(1.0)                  # Use eel.sleep(), not time.sleep()

try:
    _thread.start_new_thread( webServer,() ) # launch the server in parallel
    print("webServer started !")
except:
   print ("Error: unable to start thread")

if __name__ == "__main__":
    # We create our senders
    maze = PyramidalMaze(width) 
    scout1 = Scout("lmscout1@conversejs.org", "woweygiowa96")
    engineer1 = Engineer("lmengineer1@conversejs.org","woweygiowa96")
    worker1 = Worker("lmworker1@conversejs.org","woweygiowa96")

    scout1.constructor(maze,eel)
    scout1.start()

    engineer1.constructor(maze,eel)
    engineer1.start()

    worker1.constructor(maze,eel)
    worker1.start()

