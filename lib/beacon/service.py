import yaml
import json
import os
import time
import logging
import checks
import email


logging.getLogger(__name__).addHandler(logging.NullHandler())


class BeaconService(object):
    '''Beacon service for alerting based on location rules.'''

    def __init__(self, conf_path='/etc/beacon/settings.yaml'):
        '''Import settings and checks.'''
        with open(conf_path, 'r') as file_:
            settings = yaml.load(file_)

        self.gps_dir = settings.get('gps_dir', '')
        self.email_settings = settings.get('email_settings', {})
        self.interval = settings.get('interval', 60)

        self.last_positions = {}
        self.positions = {}

        check_classes = {
            'location': checks.LocationCheck,
            'nearby': checks.NearbyCheck,
            'moved': checks.MovedCheck,
        }
        self.checks = []
        checks_path = settings.get('checks_path', '')
        for filename in os.path.lsdir(checks_path):
            path = os.path.join(checks_path, filename)
            if not os.path.isfile(path):
                continue
            with open(path, 'r') as file_:
                config = yaml.load(file_)
            type_ = config.get('type')
            if type_ not in self.check_classes:
                continue
            self.checks.append(check_classes.get(type_)(config))

    def run(self):
        while True:
            self.update_positions()
            self.check_rules()
            time.sleep(self.interval)

    def check_rules(self):
        logging.info('Checking rules')
        if not self.last_positions:
            logging.debug('No previous positions')
            return None
        for check in self.checks:
            check.run(self.last_positions, self.positions)
            if check.is_triggered:
                self.notify(check)

    def update_positions(self):
        '''Update everyone's positions from json files.'''

        def load_position(self, name):
            '''Load a position given a name.'''
            path = os.path.join(self.gps_dir, '{}.json'.format(name))
            if not os.path.isfile(path):
                return None
            with open(path, 'r') as file_:
                return json.load(file_)

        self.last_positions = self.positions.copy()
        logging.debug('Last positions: %s', str(self.last_positions))
        filenames = os.listdir(self.gps_dir)
        names = [n.partition('.')[0] for n in filenames]
        # Remove old names
        for name in set(self.positions.keys()).difference(names):
            self.positions.pop(name, None)
        for name in names:
            if not name:
                continue
            position = self.load_position(name)
            if position:
                self.positions[name] = position
        logging.debug('Positions updated: %s', str(self.positions))

    def notify(self, check):
        logging.info('Sending notification: %s', check.status)
        from_ = self.email_settings.get('from', '')
        api_key = self.email_settings.get('api_key', '')
        domain = self.email_settings.get('domain', '')
        emailer = email.Emailer(domain, api_key)
        status = emailer.send(from_, check.email_alert_list, check.status,
                              html=check.render_message('html'))
        return status.ok
