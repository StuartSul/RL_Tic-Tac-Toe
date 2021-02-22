class Traces:
    """Traces of all movements made by players"""
    def __init__(self):
        self.traces = []

    def __str__(self):
        traces_str = ''
        for index, trace in enumerate(self.traces):
            traces_str += Traces.format_trace(index + 1, trace) + '\n'
        return traces_str

    def __repr__(self):
        return self.__str__()

    def push(self, status, i, j):
        self.traces.append((status, i, j))

    def peek(self):
        return self.traces[-1]

    def size(self):
        return len(self.traces)
    
    def clear(self):
        self.traces = []

    @staticmethod
    def format_trace(index, trace):
        return 'Move {}: ({}, {}) by player {}'.format(index, trace[1], trace[2], trace[0])