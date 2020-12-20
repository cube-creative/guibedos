import sys
from subprocess import Popen, PIPE
from unittest import TestCase


COMMAND = [sys.executable, '-m', 'guibedos.analytics', 'Analytics Script', '_analytics_script.py']


class TestAnalytics(TestCase):

    def testAll(self):
        process = Popen(
            COMMAND,
            stdout=PIPE, stderr=PIPE
        )
        stdout, stderr = process.communicate()

        print(stdout)
        print(stderr)
