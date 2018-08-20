import Fancy_progressbar as bar
import time, threading
import random as rd
bars = [bar.Progress_bar(taskname=str(i)) for i in range(10)]
fam = bar.Progress_bar_family(bars, taskname="test")
bars1 = [bar.Progress_bar(taskname=str(i)) for i in range(10)]
fam1 = bar.Progress_bar_family(bars1, taskname="test")

fam2 = bar.Progress_bar_family([fam, fam1], taskname="test")
barh = bar.Progress_bar_handler([fam,fam2])
barh.start()

for i in range (20):
    bars[rd.randint(0,len(bars)-1)].update(rd.randint(0,100))
    time.sleep(0.5)
    bars1[rd.randint(0,len(bars)-1)].update(rd.randint(0,100))
    time.sleep(0.5)
barh.stop()