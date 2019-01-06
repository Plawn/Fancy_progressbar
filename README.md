A python multi-progress bar handler

[Latest Version = 1.7]
=============
[Installation]
=============
```shell
	pip install Fancy_progressbar
```

[How to use]
=============
```python
	import Fancy_progress_bar as bar
	bar_handler = bar.Progress_bar_handler()
	some_bar = bar.Progress_bar()
	or 
	bar_handler.append(some_bar,some_other_bar)
	or 
	bar_handler.append(list=[some_bar,some_other_bar])
	bar_handler.start()
	#to update the bar you just use the method update
	some_bar.update(some_float)

	#To kill the handler use the method kill
	bar_handler.kill()
```

[Optional]
=============
Create an option object :
```python
	options = bar.Progress_bar_options("kill_when_finished","animated",taskname="bar_name",animation=["a","b"]) # without animation set there is a default animation
	some_bar = bar.Progress_bar(options=options)
	or 
	some_bar = bar.Progress_bar(options)
	or
	some_bar = bar.Progress_bar("kill_when_finished","animated",taskname="bar_name",animation=["a","b"]) 
```
Or
```python
	some_bar = bar.Progress_bar()
	some_bar.set_options(options)
```

#[Others Options]
=============
You can append multiple bars to the handler :
```python
	bar_handler.append(bar1,bar2)
	bar_handler.append(list=[bar1,bar2])
```

#[Methods available]
=============

	
```python
	#[Progress_bar]
		update(type:float)	#updates the bar to the float
		set_options(type:Fancy_progressbar.Progress_bar_options) #sets options using an option object
		kill_when_finished()	#kill the handler its located in when finished method is called
		style(type:Fancy_term.Style)	#sets a style from the Fancy_term lib
		no_style()	#removes the style
		name(type:string) #sets the naùe of the bar
		done() #sets done attribute to true
		is_done() #reads done attribute
		is_finished() #reads finished attribute
		hide()
		show()
		delete()
		finish()	
		current(string)	#sets the current task on a second line under the bar
		text(string)	#sets text on a bar
		blank()	#sets a blank bar
		text(string)  #sets a bar with the string (can be used to print text while having bars)
	
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
		stop() #same as kill
		exchange_by_index(index1,index2) #exchange the order of the bar --> changes display order
		exchange_by_bar(bar1,bar2)
		start() #starts the handler



```

New
===

* Families are now available, you have append multiples bars to a family and the renderer will take care to render everyone in the correct place.

* If you have threads launching threads then you can use a family to monitor the whole progress of your task. You just have to update the childs bar and the family will update itself.

* You can append families to families.

* The bars and families will appear under a family top bar and will be indented

```python
import Fancy_progressbar as bar


bars = [bar.Progress_bar(taskname=str(i)) for i in range(10)]
family = bar.Progress_bar_family(*bars,taskname="parent_family")
# or 
family = bar.Progress_bar_family(list=bars)
bar_handler = bar.Progress_bar_handler(family)
bar_handler.start()

```