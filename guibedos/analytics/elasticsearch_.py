import logging
from datetime import datetime

import elasticsearch


class Elasticsearch:
    def __init__(self, host):
        self.connection = elasticsearch.Elasticsearch(host)

    def save(self, report):
        logging.info('Analytics : saving session data to Elasticsearch')

        timestamp = datetime.fromtimestamp(report['start_time']).astimezone().isoformat()

        self.connection.index(
            index='guibedosanalytics_session',
            body={
                'timestamp': timestamp,
                'name': report['name'],
                'exit_code': not report['exit_code'],
                'duration': report['session_duration']
            }
        )

        for name, details in report['calls'].items():
            details.update(
                session=report['name'],
                timestamp=timestamp
            )
            self.connection.index(
                index='guibedosanalytics_call',
                body=details
            )
