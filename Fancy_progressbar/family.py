from .bar import ProgressBar


class ProgressBarFamily:
    def __init__(self, *args, **kwargs):
        self.bars: List[ProgressBar] = []
        self.is_child = False
        self.progress = 0
        self.coeff = 0
        self.is_set = False
        self.level = 0
        self.append(*args, **kwargs)
        self.family_set = False
        self._task_name: str = kwargs.get('taskname', '')
        self.task_name = ''
        self.set_taskname()
        self.top_bar = ProgressBar(**kwargs.get('bar_options', {}))
        self.set_childs()
        self.finished = False

    def set_taskname(self):
        self.task_name = '  ' * self.level + self._task_name + ' :'

    def __iter__(self):
        for bar in self.bars:
            yield bar

    def __repr__(self):
        return 'Family: {}'.format(self.task_name)

    def finish(self):
        self.finished = True
        self.top_bar.finish()

    def set_childs(self, childs=None):
        if self.is_child:
            self.top_bar.level = self.level
            self.top_bar.set_taskname()
        if childs is None:
            childs = self.bars
        for bar in childs:
            bar.level = self.level + 1
            bar.set_taskname()
            bar.set_child()
            if isinstance(bar, ProgressBarFamily):
                bar.set_childs()

    def set_child(self):
        self.is_child = True

    def current(self, string):
        self.top_bar.current(string)

    def append(self, *args, **kwargs):
        progress_bar_list = kwargs.get('list', []) + [*args]
        for bar in progress_bar_list:
            self.bars.append(bar)
            bar.to_suppr = self.bars
        self.set_childs(progress_bar_list)

    def update(self, u=None):
        self.progress, n = 0, len(self.bars)
        for bar in self.bars:
            self.progress += bar.progress / n
        self.top_bar.update(self.progress)
