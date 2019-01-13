#Declaration of all the sender and receiver classes from scouts, workers and engineers
from scout.recScout import ReceiverScout
from scout.sendScout import PeriodicSenderScout
from maze.PyramidalMaze import PyramidalMaze
# maz = PyramidalMaze(9)
import time
if __name__ == "__main__":
    receiveragent = ReceiverScout("lmworker1@conversejs.org", "woweygiowa96")
    receiveragent.start()
    senderagent = PeriodicSenderScout("lmscout1@conversejs.org", "woweygiowa96")
    senderagent.start()

    while receiveragent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            senderagent.stop()
            receiveragent.stop()
            break
    print("Agents finished")