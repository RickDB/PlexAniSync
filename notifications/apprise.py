import apprise

from misc.log import logger

log = logger.get_logger(__name__)


class Apprise:
    NAME = "Apprise"

    # initialize apprise

    def __init__(self, url, title='PlexAniSync'):
        self.url = url
        self.title = title
        log.debug("Initializing Apprise Notification Agent")

    def send(self, **kwargs):
        if not self.url:
            log.error("You must specify a url when initializing the class")
            return False

        # Send Notif

        try:
            app_obj = apprise.Apprise()
            app_obj.add(self.url)
            app_obj.notify(
                title=self.title,
                body=kwargs['message'],
            )
        except Exception:
            log.exception("Error sending notification to %r", self.url)
        return False
