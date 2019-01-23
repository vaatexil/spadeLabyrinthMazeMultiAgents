# Declaration of all the sender and receiver classes from scouts, workers and engineers
import time
from scout.scout import ReceiverScout
from scout.scout import PeriodicSenderScout
from maze.PyramidalMaze import PyramidalMaze

import eel

eel.init('web')

@eel.expose                         # Expose this function to Javascript
def say_hello_py(x):
    print('Hello from %s' % x)

say_hello_py('Python World!')
eel.updateMaze('Python World!')   # Call a Javascript function

web_app_options = {
    'mode': "chrome-app", #or "chrome"
    'port': 8080,
    'chromeFlags': ["--start-fullscreen", "--browser-startup-dialog"]
}


if __name__ == "__main__":
    receiveragent = ReceiverScout("lmworker1@conversejs.org", "woweygiowa96")
    receiveragent.start()
    senderagent = PeriodicSenderScout("lmscout1@conversejs.org", "woweygiowa96")
    maze = PyramidalMaze(9) # we create our maze
    senderagent.constructor(maze,eel)
    senderagent.start()

    eel.start('main.html', options=web_app_options)           # Start (this blocks and enters loop)

