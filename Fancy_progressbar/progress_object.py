

class Progress:
    def __init__(self):
        self._progress = 0

    def get_progress(self) -> int:
        return self._progress

    def set_progress(self, n: int) -> None:
        self._progress = n
