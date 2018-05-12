from time import sleep
import sys
import os
from threading import Thread, Event


"""
	Written by <Plawn>
"""



def console_write(string):
	sys.stdout.write(string)
	sys.stdout.flush()

clear = lambda: os.system('cls' if os.name=='nt' else 'clear')

def clear_line():
	# rows, length = os.popen('stty size', 'r').read().split()
	# length = int(length)
	length = length_of_terminal()
	console_write("\r" + " "*(length))
	
def clear_n_lines(n):
	for i in range (n):
		clear_line()
		down()	
	for i in range (n):
		up()


def up():
    console_write('\x1b[1A')
    # sys.stdout.write('\x1b[1A')
    # sys.stdout.flush()

def down():
    console_write('\n')
    # I could use '\x1b[1B' here, but newline is faster and easier
    # sys.stdout.write('\n')
    # sys.stdout.flush()


def length_of_terminal():
	# columns = int(subprocess.check_output(['stty', 'size']).decode().split()[1]) #linux and osx only
	columns = os.get_terminal_size().columns #should be bulletproof
	return(columns)

def rows_of_terminal():
	rows = os.get_terminal_size().lines
	return(rows)


class Progress_bar_options():
	def __init__(self,*args,**kwargs):
		self.options = {"taskname":'',"current":'',"style":"","max_lenght":None}
		self._options = ['hidden','blank','done','pointer',"kill_when_finished"]
		self._args = []
		self.dict = {}
		self.add_argument(args=args,dict=kwargs)
	def add_argument(self,*args,**kwargs):
		args = kwargs.get('args',args)
		kwargs = kwargs.get('dict',kwargs)
		for item in args:
			if item in self._options:
				self._args.append(item)
		for item in kwargs:
			self.options.update({item:kwargs[item]})
		self.dict = {"args":self._args,"kwargs":self.options}

	def display(self):
		print(self.options)
		print(self._args)

class Progress_bar():
	def __init__(self,*args,**kwargs):
		

		self.task_name = kwargs.get('taskname', '') + " :"
		self.fill      = kwargs.get('fill', '█')[0] if len(kwargs.get('fill', '█')) > 0 else '█'
		self.done      = False
		self.hidden    = True if "hidden" in args else False
		self.textd = kwargs.get("text","")
		self.text_only = True if len(self.textd) > 0 else False
		self.blankk    = True if "blank" in args else False
		self.pointer   = True if "pointer" in args else False #not supported yet
		self._style     = ""			#terminal colors
		self.end_style  = ""			#terminal colors
		self._kill_when_finished = True if "kill_when_finished" in args else False
		self._current   = ''
		self.progress  = 0
		self.finished  = False
		self._updated   = False
		self.event_kill = None
		self.kill_sleep = 0.001
		self._end_style = "\033[m" #terminal colors
		self.current_activated   = False
		self.max_lenght = None
		self.style(kwargs.get('style', '') )
		# <------------------>
		options = kwargs.get('options',None)
		if options != None:
			self.set_options(options)
			# print("setting options")
	def set_options(self,options):
		if "hidden" in options.dict["args"]:
			self.hidden = True
		if "blank" in options.dict["args"]:
			self.blankk = True
		if "done" in options.dict["args"]:
			self.done = True
		if "pointer" in options.dict["args"]:
			self.pointer = True
		if "kill_when_finished" in options.dict["args"]:
			self._kill_when_finished = True
		self.task_name = options.dict["kwargs"].get('taskname', '') + " :"
		self.fill	   = options.dict["kwargs"].get('fill', '█')[0] if len(options.dict["kwargs"].get('fill', '█')) > 0 else '█'
		self.textd     = options.dict["kwargs"].get('text', '')
		self.max_lenght = options.dict["kwargs"].get('max_lenght', None)
		if len(self.textd) > 0:
			self.text_only = True
		self.style(options.dict["kwargs"].get('style', '') )
		self.current_task(str(options.dict["kwargs"].get('current', '')))
		# print(self.blankk,self.text_only,self.textd,self._kill_when_finished)
	def kill_when_finished(self):
		self._kill_when_finished = True
	def no_style(self):
		self._style = ""
		self.end_style = ""
	def style(self,style):
		if "Style" in str(type(style)):
			self.end_style = self._end_style
			self._style = style.str()
		else:
			if len(style) > 0 :
				self.end_style = self._end_style
				self._style = style
	def hide(self):
		self.hidden = True
	def show(self):
		self.hidden = False
	def delete(self):
		self.done = True
		self.hidden = True
	def finish(self,**kwargs):
		if self.event_kill != None and self._kill_when_finished:
			self.event_kill.set()
		if not self.current_activated:
			if kwargs.get('showing', False) or kwargs.get('message') != None:
				self._current           = kwargs.get('message', 'Done')
				self.current_activated = True
		else:
			self._current           = kwargs.get('message', 'Done')
			self.current_activated = True
		self.finished          = True
		if self._kill_when_finished:
			sleep(0.001)
	def current(self,currentt):
		if len(currentt) > 0 :
			self._current = str(currentt)
			self.current_activated = True
	def text(self,string):
		self.text_only = True
		self.textd     = string
	def blank(self):
		self.text_only = True
		self.blankk    = True
	def update(self,progress):
		self.progress = progress
		self._updated  = True

	def print_bar(self):
		if self.pointer :
			try :
				progress = self.progress[0] #not working now 
			except :
				raise ValueError
				self.done = True
		else:
			progress = self.progress
		# self.length = int(os.popen('stty size', 'r').read().split()[1]) #windows command must be added
		if self.max_lenght != None:
			l = length_of_terminal() 
			if l < self.max_lenght:
				length = l
			else:
				length = self.max_lenght
		else:
			length = length_of_terminal()
		
		output = "\r" + self._style
		if not self.text_only:
			dec = str(int(int((progress % 1) *100)))
			if len(dec) == 1 :
				dec += '0'
			
			progress_str = str(int(progress)) + dec
			length       = int(length)-len(self.task_name)-len(str(progress_str))-len(dec)-3
			if progress > 100 :
				filledLength = length
			else:
				filledLength = int(length * progress / 100)
			
			bar   = self.task_name + self.fill * filledLength + '-' * (length - filledLength) + " " + str(int(progress))+ '.' +str(dec) + "%"
			
			if not self.current_activated :
				output += bar 
			else:
				output += bar + "\n" + str(self._current) + " "*(length-len(str(self._current)))
		else:
			if not self.blankk :
				if len(self.textd) > length :

					output += self.textd[0:length] + self.end_style
				else :
					output += self.textd +" "*(length-len(str(self.textd)))
			else:
				return("\r" + " "*length)
		output += self.end_style
		return(output)
		

	
class Progress_bar_handler(Thread):
	def __init__(self,progress_bar_list=[],*args,**kwargs):
		Thread.__init__(self)
		self.event_kill = Event()
		self.event_on_change = Event()
		self.progress_bar_list  = progress_bar_list
		# self.actualisation_time = 0.5
		self.dead               = False
		self.paused             = False
		self.old_lines          = 0
		self.default_kill_sleep = 0.001
		presets = {'fast':0.1,'very fast':0.01,"slow":1,'very slow':3,'medium':0.8,'default':0.5}
		self.actualisation_time = kwargs.get('refresh', 0.5)
		# for sig in ('TERM', 'HUP', 'INT'):
		# 	signal.signal(getattr(signal, 'SIG'+sig), quit)
		try :
			self.preset = kwargs['preset']
			try :
				self.actualisation_time = presets[self.preset]
			except :
				print('preset unknown -> will use default settings aka 0.5')
		except :
			pass
		
	def append(self,*progress_bar):
		for i in progress_bar :
			if 'list' in str(type(i)):
				for bare in i :
					if bare not in self.progress_bar_list :
						self.progress_bar_list.append(bare)
						bare.event_kill = self.event_kill
						bare.kill_sleep = self.default_kill_sleep
			else:
				if i not in self.progress_bar_list :
					self.progress_bar_list.append(i)
					i.event_kill = self.event_kill
					i.kill_sleep = self.default_kill_sleep
	def remove(self,progress_bar):
		try :
			self.progress_bar_list.remove(progress_bar)
			return(True)
		except :
			return(False)
	def pause(self):
		self.paused = True
	def resume(self):
		self.paused = False
	def kill(self):
		self.event_kill.set()
		sleep(self.default_kill_sleep)
	def list(self):
		return(self.progress_bar_list)
	def exchange_by_index(self,index1:int,index2:int):
		try :
			self.progress_bar_list[index1], self.progress_bar_list[index2] = self.progress_bar_list[index2], self.progress_bar_list[index1]
			return(True)
		except :
			return(False)
	def exchange_by_bar(self,bar1,bar2):
		try :
			index1, index2  = self.progress_bar_list.index(bar1),self.progress_bar_list.index(bar2)
			self.exchange_by_index(index1,index2)
			return(True)
		except :
			return(False)


	def run(self):
		line = 1
		last_one = False
		while not self.event_kill.is_set() or not last_one:
			
			if not self.paused :
				max_line = rows_of_terminal()
				line = 0
				new_line = len(self.progress_bar_list[0:max_line])
				for bar in self.progress_bar_list[0:max_line] :
					if not bar.hidden :
						new_line += 1
						if bar.current_activated :
							new_line += 1
				if new_line != self.old_lines :
					clear_n_lines(self.old_lines)
					self.old_lines = new_line

				for bar in self.progress_bar_list[0:max_line] :
					# if bar._kill_when_finished :
					# 	if bar.finished :
					# 		self.event.set()


					if not bar.hidden :
						line += 1
						if not bar.done :
							# line += 1
							if bar.current_activated :
								line += 1
							string = bar.print_bar()
							console_write(string)
							down()
						else:
							down()
							for a_bar in self.progress_bar_list[0:max_line] :
								down()
								clear_line()
								if bar.current_activated :
									down()
									clear_line()
							for a_bar in self.progress_bar_list[0:max_line] :
								up()
								if bar.current_activated :
									up()
							self.progress_bar_list.remove(bar)
				if new_line > max_line :
					lenght = length_of_terminal()
					console_write(" v" * (int(lenght/2) -1 ))
				for i in range (line) :
					up()	
			if self.event_kill.is_set():
				last_one = True
			else:
				self.event_kill.wait(self.actualisation_time)
			
		
		for i in range (line):
			console_write("\n")
		self.dead = True
		# print("shutdown complete")
		

