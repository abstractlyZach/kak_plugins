class FakeKakState(object):
    def __init__(self, buffer_path=None, selection=None):
        self._buffer_path = buffer_path
        self._selection = selection

    @property
    def buffer_path(self):
        return self._buffer_path

    @property
    def selection(self):
        return self._selection


class FakeSelectionDescription(object):
    def __init__(self, to_str):
        self._to_str = to_str

    def __str__(self):
        return self._to_str
