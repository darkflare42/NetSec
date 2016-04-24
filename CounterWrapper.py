
class CounterWrapper:
    def __init__(self):
        self._counter = 0

    def increment(self):
        self._counter += 1

    def get_value(self):
        return self._counter
