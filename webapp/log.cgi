#!/usr/bin/env python

'''Logs gps coordinates for beacon.'''

import cgi
import json
import yaml
import os
import logging
from firebase import firebase


def parse_float(string_):
    '''Parse float from string.'''
    try:
        return float(string_)
    except ValueError:
        return None


def save_data_local(data, logger):
    '''Save data to beacon working dir.'''
    data_dir = get_setting('gps_dir')
    if os.path.isdir(data_dir):
        path = os.path.join(data_dir, '{}.json'.format(data.get('id')))
        logger.info('Writing data to: %s data: %s', path, str(data))
        with open(path, 'w') as file_:
            json.dump(data, file_)


def save_data_firebase(data, logger):
    '''Save data to firebase.'''
    firebase_settings = get_setting('firebase')
    auth = firebase.FirebaseAuthentication(firebase_settings.get('secret', ''), '')
    db = firebase.FirebaseApplication(
        'https://{}.firebaseio.com'.format(firebase_settings.get('project')),
        authentication=auth)
    data['time'] = {'.sv': 'timestamp'}
    db.put('/positions', data.get('id', ''), data)


def get_setting(key, path='/etc/beacon/settings.yaml'):
    '''Get setting from settings.yaml.'''
    if os.path.isfile:
        with open(path, 'r') as file_:
            settings = yaml.load(file_)
            return settings.get(key, '')
    else:
        return None


def main():
    '''Log gps data.'''
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(message)s',
        '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    valid_ids = get_setting('valid_ids')
    args = cgi.FieldStorage()
    lat = parse_float(args.getfirst('lat'))
    lon = parse_float(args.getfirst('lon'))
    speed = parse_float(args.getfirst('s'))
    id_ = args.getfirst('id')

    print 'Content-Type: application/json\n'
    data = {
        'id': id_,
        'lat': lat,
        'lon': lon,
        'speed': speed,
    }
    if None not in (lat, lon, speed, id_) and id_ in valid_ids:
        save_data_firebase(data, logger)
        print json.dumps({'status': 'ok'})
    else:
        logger.info('Error saving data: %s', str(data))
        print json.dumps({'status': 'error', 'data': data})


if __name__ == '__main__':
    main()
