# coding=utf-8
import logging
import time

from io import StringIO
from requests import get, HTTPError

logger = logging.getLogger("PlexAniSync")
# Gets overriden by settings.ini
settings = {
    'enabled': False,
    'errors_only': False,
    'bot_token': '',
    'chat_id': '',
}

# Keep track of errors for Telegram integration
error_tracker = StringIO()
handler = logging.StreamHandler(error_tracker)
handler.setLevel(logging.WARNING)
logger.addHandler(handler)


def setup(ini_settings):
    global settings
    if ini_settings.get('enabled', '').lower().strip() == 'true':
        enabled = True
        bot_token, chat_id = ini_settings.get('bot_token', '').strip(), ini_settings.get('chat_id').strip()

        if not bot_token:
            logger.error('[TELEGRAM] Bot token not set, disabling telegram integration')
            enabled = False
        if not chat_id:
            logger.error('[TELEGRAM] Chat id not set, disabling telegram integration')
            enabled = False

        settings['enabled'] = enabled
        settings['bot_token'] = bot_token
        settings['chat_id'] = chat_id
        settings['errors_only'] = ini_settings.get('errors_only', '').lower().strip() == 'true'


def send_message(text):
    if not settings['enabled']:
        return

    log_text = text if len(text) < 30 else (text[:27] + '...')
    try:
        response = get(
                f'https://api.telegram.org/bot{settings["bot_token"]}/sendMessage',
                data={
                    'chat_id': settings['chat_id'],
                    'text': text,
                    'parse_mode': 'markdown'
                })
        response.raise_for_status()
        logger.info(f'[TELEGRAM] message sent to Telegram | chat_id: {settings["chat_id"]} | text: "{log_text}"')
    except HTTPError as e:
        logger.error(f'[TELEGRAM] Could not send message | chat_id: {settings["chat_id"]} | text: "{log_text}" | error: {e}')


def starting_sync(version):
    if not settings['enabled'] or settings['errors_only']:
        return

    send_message(f'PlexAniSync - version: `{version}`\nSync Started - `{time.asctime()}`')


def report_to_telegram():
    if not settings['enabled']:
        return

    if error_tracker.getvalue():
        error = ''
        for line in error_tracker.getvalue().split('\n'):
            if len(error) + len(line) + 3 > 4096:
                send_message(error)
                error = ''
            error += f'`{line}`\n'
        if error:
            send_message(error)

    if not settings['errors_only']:
        send_message(f'Sync Complete - `{time.asctime()}`')
