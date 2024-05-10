import logging
from ddtrace import tracer

class DataDogLogger:
    def __init__(self, service_name: str):
        self.logger = logging.getLogger(service_name)
        self.logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.service_name = service_name

    def log(self, level: str, message: str):
        log_method = getattr(self.logger, level.lower(), None)
        if log_method is not None:
            log_method(message)

        with tracer.trace(f"{self.service_name}.{level}", service=self.service_name):
            tracer.current_span().set_tag("message", message)
