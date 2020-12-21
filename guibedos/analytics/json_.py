import json
import logging


class JSON:
    def __init__(self, filepath):
        self.filepath = filepath

    def save(self, report):
        logging.info('Analytics : saving session data to {}'.format(self.filepath))

        with open(self.filepath, "w+") as f_json:
            json.dump(report, f_json, indent=2)
