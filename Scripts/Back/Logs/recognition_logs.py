from Scripts.Utils.events_handler import dispatch_event


class RecognitionLogs:
    logs = []

    def add(self, query: str):
        self.logs.append(query)
        dispatch_event('logs_updated', logs=self.get_logs())

    def get_logs(self):
        return self.logs
