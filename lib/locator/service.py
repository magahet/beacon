import yaml
import json
import os
import math
import time
import email
import logging


logging.getLogger(__name__).addHandler(logging.NullHandler())


class LocationService(object):
    '''Locator service for alerting based on location rules.'''

    def __init__(self, conf_path='/etc/locator/settings.yaml'):
        with open(conf_path, 'r') as file_:
            settings = yaml.load(file_)
        self.locations_path = settings.get('locations_path', '')
        self.gps_dir = settings.get('gps_dir', '')
        self.email_settings = settings.get('email_settings', {})
        self.interval = settings.get('interval', 60)
        self.last_positions = {}
        self.positions = {}
        self.locations = []

    def run(self):
        self.update_locations()
        while True:
            self.update_positions()
            self.check_rules()
            time.sleep(self.interval)

    def check_rules(self):
        logging.info('Checking rules')
        if not self.last_positions:
            logging.debug('No previous positions')
            return None
        for location in self.locations:
            logging.debug('Checking location: %s', str(location))
            self.check_positions(location)

    def in_location(self, position, location):
        point1 = (position.get('lat'), position.get('lon'))
        point2 = (location.get('lat'), location.get('lon'))
        radius = location.get('radius')
        distance = self.distance(point1, point2)
        logging.debug('Distance between %s and %s is %d.', str(point1),
                      str(point2), distance)
        return distance < radius

    @staticmethod
    def distance(point1, point2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        Returns meters
        """
        # convert decimal degrees to radians
        lat1, lon1 = point1
        lat2, lon2 = point2
        lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(lat1) *
             math.cos(lat2) *
             math.sin(dlon / 2) ** 2)
        c = 2 * math.asin(math.sqrt(a))
        r = 6371000  # Radius of earth in kilometers. Use 3956 for miles
        return c * r

    def check_positions(self, location):
        for name, position in self.positions.iteritems():
            last_position = self.last_positions.get(name)
            logging.debug('Checking: %s, %s, %s', name, position, last_position)
            if not last_position:
                continue
            was_in = self.in_location(last_position, location)
            is_in = self.in_location(position, location)
            if not was_in and is_in:
                self.notify(name, position, location, 'entered')
            elif was_in and not is_in:
                self.notify(name, position, location, 'left')

    def update_positions(self):
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

    def notify(self, name, position, location, action):
        subject = '{name} {action} {location}'.format(
            name=name,
            action=action,
            location=location.get('name', ''))
        logging.info('Sending notification: %s', subject)
        message = (
            '<html>'
            '{name} {action} {location} ({radius}m) at {time}.</br>'
            'Position: {position}.</br>'
            '<a href="{map_url}/?q={lat},{lon}">'
            '<img ng-src="{map_url}/api/staticmap'
            '?center={lat},{lon}'
            '&size=400x400'
            '&zoom=14'
            '&markers={lat},{lon}">'
            '</img></a>'
        ).format(
            name=name,
            action=action,
            location=location.get('name', ''),
            radius=location.get('radius', ''),
            position=str(position),
            time=position.get('time', ''),
            map_url='http://maps.googleapis.com/maps',
            lat=position.get('lat', ''),
            lon=position.get('lon', '')
        )
        to_ = location.get('email', '')
        from_ = self.email_settings.get('from', '')
        api_key = self.email_settings.get('api_key', '')
        _, _, domain = from_.partition('@')
        emailer = email.Emailer(domain, api_key)
        status = emailer.send(from_, to_, subject, html=message)
        return status.ok

    def load_position(self, name):
        path = os.path.join(self.gps_dir, '{}.json'.format(name))
        if not os.path.isfile(path):
            return None
        with open(path, 'r') as file_:
            return json.load(file_)

    def update_locations(self):
        if not os.path.isfile(self.locations_path):
            return []
        with open(self.locations_path, 'r') as file_:
            self.locations = yaml.load(file_)
        logging.info('Imported locations: %s', str(self.locations))
