import sys
import logging
import argparse

from guibedos.analytics.runner import Runner


def parse_args(args):
    parser = argparse.ArgumentParser(
        prog='python -m guibedos.analytics',
        description='Wrap a python command to parse analytics log messages'
    )

    parser.add_argument(
        '-n', '--name',
        type=str,
        required=True,
        help='application name'
    )

    parser.add_argument(
        '-j', '--json',
        type=str,
        required=False,
        help='JSON filepath to output report to'
    )
    parser.add_argument(
        '-e', '--elasticsearch',
        type=str,
        help='host to elasticsearch to save report to'
    )

    return parser.parse_known_args(args)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    parsed_args, command = parse_args(sys.argv[1:])

    runner = Runner(parsed_args.name)
    report = runner.run([sys.executable] + command)

    if parsed_args.json:
        from guibedos.analytics.json_ import JSON

        json = JSON(parsed_args.json)
        json.save(report)

    if parsed_args.elasticsearch:
        from guibedos.analytics.elasticsearch_ import Elasticsearch

        elasticsearch = Elasticsearch(parsed_args.elasticsearch)
        elasticsearch.save(report)

    sys.exit(report['exit_code'])
