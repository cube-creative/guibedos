import sys
from guibedos.analytics.runner import Runner


if __name__ == '__main__':
    app_name = sys.argv[1]
    actual_command = [sys.executable] + sys.argv[2:]

    runner = Runner(app_name)
    report = runner.run(actual_command)

    sys.exit(runner.exit_code)
