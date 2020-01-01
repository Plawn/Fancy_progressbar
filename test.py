import Fancy_progressbar as fp



o = fp.Progress()
o.set_progress(10)

b = fp.ProgressBar('test', 'kill_when_finished', 'animated')
b.use_progress(o)
bh = fp.ProgressBarHandler([b])

bh.start()