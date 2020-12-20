import re
import time

from .constants import *
from .subprocess_async import run


_RE_REGISTER = re.compile(REGISTER_PATTERN)
_RE_CALL = re.compile(CALL_PATTERN)


class Runner:
    def __init__(self, name):
        self.end_time = 0
        self.start_time = 0
        self.session_duration = 0
        self.name = name
        self.calls = dict()
        self.exit_code = None

    @property
    def report(self):
        return vars(self)

    def process_output(self, line):
        line = line.decode()

        for registered in _RE_REGISTER.findall(line):
            self.calls[registered] = {'calls': list()}

        for called in _RE_CALL.findall(line):
            name, duration, error = called
            self.calls[name]['calls'].append((
                float(duration),
                not error
            ))

    def _make_stats(self):
        self.session_duration = self.end_time - self.start_time

        for name, data in self.calls.items():
            count = len(data['calls'])

            if count:
                total_time = sum(call[0] for call in data['calls'])
                average = total_time / count
                ratio = total_time / self.session_duration
                exception_count = count - sum(call[1] for call in data['calls'])
            else:
                total_time = 0
                average = 0
                ratio = 0
                exception_count = 0

            self.calls[name] = {
                'name': name,
                'time_ratio': ratio,
                'total_time': total_time,
                'average': average,
                'count': count,
                'exception_count': exception_count
            }

    def run(self, command):
        self.start_time = time.time()
        self.exit_code = run(command, stderr_callback=self.process_output)
        self.end_time = time.time()

        self._make_stats()

        return self.report
