class ProgressBarOptions():
    
    default_animation = ["[|]", "[/]", "[-]", "[\\]"]
    
    def __init__(self, *args, **kwargs):
        
        self.options = {"taskname": '', "current": '',
                        "style": "", "max_length": None, "animation": self.default_animation}
        self._options = ['hidden', 'blank', 'done',
                         'pointer', "kill_when_finished", "animated"]
        self._args = []
        self.dict = {}
        self.add_argument(args=args, dict=kwargs)

    def add_argument(self, *args, **kwargs):
        for item in kwargs.get('args', args):
            if item in self._options:
                self._args.append(item)
        for item in kwargs.get('dict', kwargs):
            self.options[item] = kwargs[item]
        self.dict = {"args": self._args, "kwargs": self.options}

    def __repr__(self):
        return '{}\n{}'.format(self.options, self._args)