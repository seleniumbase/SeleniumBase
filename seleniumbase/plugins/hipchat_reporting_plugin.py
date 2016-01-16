""" This plugin allows you to receive test notifications through HipChat.
HipChat @ mentions will only occur during normal
business hours. (You can change this)
By default, only failure notifications will be sent.
"""

import os
import requests
import logging
import datetime
from nose.plugins import Plugin
from seleniumbase.config import settings


HIPCHAT_URL = 'https://api.hipchat.com/v1/rooms/message'
HIPCHAT_AUTH_TOKEN = settings.HIPCHAT_AUTH_TOKEN


class HipchatReporting(Plugin):
    '''
    Usage: --with-hipchat_reporting --hipchat_room_id=[HIPCHAT ROOM ID]
           --hipchat_owner_to_mention=[HIPCHAT @NAME]
    '''
    name = 'hipchat_reporting'

    def __init__(self):
        super(HipchatReporting, self).__init__()
        self.hipchat_room_id = None
        self.hipchat_owner_to_mention = None
        self.hipchat_notify_on_success = False
        self.build_url = os.environ.get('BUILD_URL')
        self.successes = []
        self.failures = []
        self.errors = []

    def options(self, parser, env):
        super(HipchatReporting, self).options(parser, env=env)
        parser.add_option(
            '--hipchat_room_id', action='store',
            dest='hipchat_room_id',
            help='The hipchat room ID notifications will be sent to.',
            default=None)
        parser.add_option(
            '--hipchat_owner_to_mention', action='store',
            dest='hipchat_owner_to_mention',
            help='The hipchat username to @mention in notifications.',
            default=None)
        parser.add_option(
            '--hipchat_notify_on_success', action='store_true',
            default=False,
            dest='hipchat_notify_on_success',
            help='''Flag for including success notifications.
                 If not specified, only notifies on errors/failures
                 by default.''')

    def configure(self, options, conf):
        super(HipchatReporting, self).configure(options, conf)
        if not self.enabled:
            return
        if not options.hipchat_room_id:
            raise Exception('''A hipchat room ID to notify must be specified
                            when using the hipchat reporting plugin.''')
        else:
            self.hipchat_room_id = options.hipchat_room_id
        self.hipchat_owner_to_mention = (
            options.hipchat_owner_to_mention or None)
        self.hipchat_notify_on_success = options.hipchat_notify_on_success

    def addSuccess(self, test, capt):
        self.successes.append(test.id())

    def addError(self, test, err, capt=None):
        self.errors.append("ERROR: " + test.id())

    def addFailure(self, test, err, capt=None, tbinfo=None):
        self.failures.append("FAILED: " + test.id())

    def finalize(self, result):
        message = ''
        success = True
        if not result.wasSuccessful():
            success = False
            if (self.hipchat_owner_to_mention and
                    self._is_during_business_hours()):
                message += "@" + self.hipchat_owner_to_mention + '\n'

            if self.failures:
                message += "\n".join(self.failures)
                if self.errors:
                    message += '\n'
            if self.errors:
                message += "\n".join(self.errors)

            if self.build_url:
                message += '\n' + self.build_url

        elif self.hipchat_notify_on_success and self.successes:
            message = "SUCCESS! The following tests ran successfully:\n+ "
            message += "\n+ ".join(self.successes)

        if message:
            self._send_hipchat_notification(message, success=success)

    def _is_during_business_hours(self):
        now = datetime.datetime.now()
        # Mon - Fri, 9am-6pm
        return now.weekday() <= 4 and now.hour >= 9 and now.hour <= 18

    def _send_hipchat_notification(self, message, success=True,
                                   sender='Selenium'):
        response = requests.post(HIPCHAT_URL, params={
            'auth_token': HIPCHAT_AUTH_TOKEN,
            'room_id': self.hipchat_room_id,
            'from': sender,
            'message': message,
            'message_format': 'text',
            'color': 'green' if success else 'red',
            'notify': '0',
            'format': 'json'
        })

        if response.status_code == 200:
            logging.debug("Notification sent to room %s", self.hipchat_room_id)
            return True
        else:
            logging.error("Failed to send notification to room %s",
                          self.hipchat_room_id)
            return False
