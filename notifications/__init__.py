from misc.log import logger
from .apprise import Apprise
from .pushover import Pushover
from .slack import Slack

log = logger.get_logger(__name__)

SERVICES = {
    'apprise': Apprise,
    'pushover': Pushover,
    'Slack': Slack
}


class Notifications:
    def __init__(self):
        self.services = []

    def load(self, **kwargs):
        if 'service' not in kwargs:
            log.error("You must specify a service to load with service parameter")
            return False
        elif kwargs['service'] not in SERVICES:
            log.error("You have specified an invalid service to load %s", kwargs['service'])
            return False

        try:
            chosen_service = SERVICES[kwargs['service']]
            del kwargs['service']

            # load the chosen service.

            service = chosen_service(**kwargs)
            self.services.append(service)

        except Exception:
            log.exception("Exception while loading the service, kwargs=%r: ", kwargs)

    def send(self, **kwargs):
        try:
            if 'service' in kwargs:
                # Remove service keyword if they have given it.
                chosen_service = kwargs['service'].lower()
                del kwargs['service']
            else:
                chosen_service = None
                # Send the notif to the specified service.

            for service in self.services:
                if chosen_service and service.NAME.lower() != chosen_service:
                    continue
                elif service.send(**kwargs):
                    log.debug("Sent Notification With %s", service.NAME)

        except Exception:
            log.exception("Exception occurred when sending notification, kwargs=%r: ", kwargs)
