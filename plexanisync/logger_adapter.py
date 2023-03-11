import logging
from typing import Tuple

class PrefixLoggerAdapter(logging.LoggerAdapter):
    """ A logger adapter that adds a prefix to every message """
    def process(self, msg: str, kwargs: dict) -> Tuple[str, dict]:
        return (f'[{self.extra["prefix"]}] ' + msg, kwargs)
