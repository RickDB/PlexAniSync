import requests

from misc.log import logger

log = logger.get_logger(__name__)


# Pushvoer Class

class Pushover:
    NAME = 'Pushover'

    # initializing
    def __init__(self, application_token, user_token, priority=0):
        self.application_token = application_token
        self.user_token = user_token
        self.priority = priority
        log.debug("Initializing Pushover Notification Agent")

    def send(self, kwargs):
        if not self.application_token or not self.user_token:
            log.error("You must specify an application token and user token when initializing this class")
            return False

        # Send notif
        try:
            load = {
                'token': self.application_token,
                'user': self.user_token,
                'message': kwargs['message'],
                'priority': self.priority,
            }
            req = requests.post('https://api.pushover.net/1/messages.json', data=load, timeout=30)
            return True if req.status_code == 200 else False

        except Exception:
            log.exception("Error sending notification to %r", self.user_token)
            return False
