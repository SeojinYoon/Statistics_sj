
import psychopy
from psychopy import visual, core

"""
- psychopy's RGB color space
    *: the space is ranged between 1 and -1(0 <-> 255, -1: 0)
    
    - [-1, -1, -1] is black
"""

# *@ checking window is opened stably
win = visual.Window(size=[100,100],
                    color = [-1,-1,-1], # black
                    colorSpace = 'rgb',
                    monitor = 'testMonitor')
win.close()

# *@ checking window can be deleted

# *@ Input test
keys = psychopy.event.waitKeys()

# *@ Input must be robust about time(So, need to check input is doing well when the time is delayed)
while True:
    keys = psychopy.event.getKeys()
    if len(keys) != 0:
        if keys[0] == "q":
            break
        else:
            print(keys[0])

# *@ I need to check the file writed by input
import csv
import time
with open('./participant_' + '.csv', 'w', newline='') as f:
    makewrite = csv.writer(f)
    makewrite.writerow(['timestep', 'stimulus', 'secs'])

    while True:
        keys = psychopy.event.getKeys()
        if len(keys) != 0:
            if keys[0] == "q":
                break
            else:
                print(keys[0])
                makewrite.writerow([0, keys[0], time.time()])
