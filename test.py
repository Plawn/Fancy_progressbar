import Fancy_progressbar as fp
import random as rd
import time

def get_progress():
    return 100 * rd.random()


b = fp.ProgressBar('test', 'kill_when_finished', 'animated')
b.use_progress(get_progress)
bh = fp.ProgressBarHandler([b])

bh.start()
time.sleep(3)
b.finish()