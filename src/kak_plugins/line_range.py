class LineRange(object):
    """Describes a range of lines, both in Kakoune and Github"""

    def __init__(self, start: int, stop: int) -> None:
        if stop < start:
            # LineRanges are dumb objects and should always have start/stop ordered
            raise ValueError(f"Invalid range. {stop} < {start}")
        if start < 1:
            # kakoune and github start their line counts at 1
            raise ValueError(f"Invalid range start. {start} < 1")
        self._start = start
        self._stop = stop

    def __str__(self) -> str:
        if self._start == self._stop:
            return f"L{self._start}"
        else:
            return f"L{self._start}-L{self._stop}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, LineRange):
            return (self._start, self._stop) == (other._start, other._stop)
        return False
