[Latest Version = 0.22]

##[Installation]

```shell
	pip install Fancy_progressbar
```

##[How to use]

```python
	import Fancy_progress_bar as bar
	bar_handler = bar.Progress_bar_handler()
	some_bar = bar.Progress_bar()
	bar_handler.append(some_bar)
	bar_handler.start()
	#to update the bar you just use the method update
	some_bar.update(some_float)

	#To kill the handler use the method kill
	bar_handler.kill()
```

#[Optional]

Create an option object :
```python
	options = bar.Progress_bar_options("kill_when_finished",taskname="bar_name")
	some_bar = bar.Progress_bar(options=options)
```
Or
```python
	some_bar = bar.Progress_bar()
	some_bar.set_options(options)
```

#[Others Options]

You can append multiple bars to the handler :
```python
	bar_handler.append(bar1,bar2)
	bar_handler.append([bar1,bar2])
```

#[Methods available]
	

	
```python
	#[Progress_bar]
		update(float)	#updates the bar to the float
		set_options(Fancy_progressbar.Progress_bar_options) #sets options using an option object
		kill_when_finished()	#kill the handler its located in when finished method is called
		style(Fancy_term.Style)	#sets a style from the Fancy_term lib
		no_style()	#removes the style
		hide()
		show()
		delete()
		finish()	
		current_task(string)	#sets the current task on a second line under the bar
		text(string)	#sets text on a bar
		blank()	#sets a blank bar
		print_bar()	#used by the handler
	
	#[Progress_bar_options]
		add_argument(*args,**kwargs)
		#can be used to set this options 
			# taskname
			# current
			# style
			# max_lenght
			# hidden
			# blank
			# done
			# pointer (not supported yet)
			# kill_when_finished
	
	#[Progress_bar_handler]
		append()
		remove()
		pause()
		resume()
		kill()
		exchange_by_index(index1,index2) #exchange the order of the bar --> changes display order
		exchange_by_bar(bar1,bar2)
		start() #starts the handler



```