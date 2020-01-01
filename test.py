import Fancy_progressbar as fp

b = fp.ProgressBar('test', 'kill_when_finished', 'animated')
bh = fp.ProgressBarHandler([b])

bh.start()