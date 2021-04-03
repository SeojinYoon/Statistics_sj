
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

def f(x):
    return 630 * ( (1/9)*(x**9) - (1/2)*(x**8) + (6/7)*(x**7) - (2/3)*(x**6) + (1/5)*(x**5) )

import numpy as np
sigma = 1/np.sqrt(44)
mu = 1/2

upper = mu + 2*sigma
lower = mu - 2*sigma

f(upper) - f(lower)


