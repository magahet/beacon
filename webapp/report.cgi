#!/usr/bin/env python

'''This script returns a json document with the current position data.'''

import cgi
import json
import os
import yaml
import hashlib
import firebase


def load_data(data_dir):
    '''Load position data.'''
    data = []
    for filename in os.listdir(data_dir):
        with open(os.path.join(data_dir, filename), 'r') as file_:
            data.append(json.load(file_))
    return data


def load_data_firebase():
    '''Save data to firebase.'''
    firebase_settings = get_setting('firebase')
    auth = firebase.FirebaseAuthentication(firebase_settings.get('secret', ''), '')
    db = firebase.FirebaseApplication(
        'https://{}.firebaseio.com'.format(firebase_settings.get('project')),
        authentication=auth)
    data = db.get('/positions', None)
    return data.values()


def hash(string):
    return hashlib.sha256(string).hexdigest()


def get_report(key):
    '''Get position report.'''
    gps_hash = get_setting('gps_hash')
    data_dir = get_setting('gps_dir')
    if hash(key) == gps_hash:
        return {
            'status': 'ok',
            'data': load_data_firebase(),
        }
    else:
        return {'status': 'unauthorized'}


def get_setting(key, path='/etc/beacon/settings.yaml'):
    '''Get setting from settings.yaml.'''
    if os.path.isfile:
        with open(path, 'r') as file_:
            settings = yaml.load(file_)
            return settings.get(key, '')
    else:
        return None


def main():
    '''Build report'''
    args = cgi.FieldStorage()
    key = args.getfirst('key', '')
    print 'Content-Type: application/json\n'
    print json.dumps(get_report(key), indent=2)


if __name__ == '__main__':
    main()
