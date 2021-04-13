import requests

from misc.log import logger

log = logger.get_logger(__name__)


class Slack:

    def __index__(self, web_hook_url, sender_name='PlexAniSync', sender_icon=':minidisc:', channel=None):
        self.web_hook_url = web_hook_url
        self.sender_name = sender_name
        self.sender_icon = sender_icon
        self.channel = channel
        log.debug("Initializing Slack Notification Agent")

    def send(self, **kwargs):
        if not self.webhook_url or not self.sender_name or not self.sender_icon:
            log.error("You must specify WebHook url, sender name and sender icon when initializing this class")
            return False

        try:
            load = {
                'text': kwargs['message'],
                'username': self.sender_name,
                'icon_emoji': self.sender_icon,
            }

            if self.channel:
                load['channel'] = self.channel

            req = requests.post(self.webhook_url, json=load, timeout=30)
            return True if req.status_code == 200 else False

        except Exception:
            log.exception("Error sending notification to %r", self.webhook_url)
        return False
