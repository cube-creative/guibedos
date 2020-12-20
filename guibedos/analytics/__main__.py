import re
import sys
from guibedos.analytics.runner import execute
from guibedos.analytics.constants import *


RE_REGISTER = re.compile(REGISTER_PATTERN)
RE_CALL = re.compile(CALL_PATTERN)


def process_output(line):
    line = line.decode()

    for registered in RE_REGISTER.findall(line):
        print(registered)

    for called in RE_CALL.findall(line):
        print(called)


if __name__ == '__main__':
    app_name = sys.argv[1]
    actual_command = [sys.executable] + sys.argv[2:]

    exit_code = execute(
        command=actual_command,
        stderr_callback=process_output
    )

    sys.exit(exit_code)
