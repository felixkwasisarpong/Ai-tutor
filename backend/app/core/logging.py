import logging
import json

logger = logging.getLogger("app")

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,

        }

        if hasattr(record, "request_id"):
            log["request_id"] = record.request_id

        if record.exc_info:
            log["exception"] = self.formatException(record.exc_info)

        return json.dumps(log)
    

def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers = [handler]
