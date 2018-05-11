How to install :
	pip install Fancy_progressbar

How to use :
	create a Progress_bar_handler :
	--> import Fancy_Progress_bar as bar
	--> bar_handler = bar.Progress_bar_handler()

	[Optional]
	create an option object :
	--> options = bar.Progress_bar_options("kill_when_finished",taskname="bar_name")

	create a Progress_bar :
	--> some_bar = bar.Progress_bar(options=options)

	or simply
	--> some_bar = bar.Progress_bar()
		some_bar.set_options(options)

	Then you can append multiple bars to the handler :
	--> bar_handler.append(bar1,bar2) or bar_handler.append([bar1,bar2])

	when all your bars are ready start the handler :
	--> bar_handler.start()