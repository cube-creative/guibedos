import sys
from unittest import TestCase

from guibedos.analytics.runner import Runner


class TestAnalytics(TestCase):

    def testAll(self):
        runner = Runner('Analytics Tests')
        report = runner.run([sys.executable, '_analytics_script.py'])

        # General
        self.assertEqual(report['name'], 'Analytics Tests')
        self.assertEqual(report['exit_code'], 1)

        # Never Used
        self.assertEqual(report['calls']['Never used']['count'], 0)

        # Five times
        self.assertEqual(report['calls']['Used five times']['count'], 5)
        self.assertEqual(report['calls']['Used five times']['exception_count'], 0)

        # Raising exception
        self.assertEqual(report['calls']['Raising exception']['count'], 1)
        self.assertEqual(report['calls']['Raising exception']['exception_count'], 1)
