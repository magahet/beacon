#!/usr/bin/env python

'''This script returns a json document with the current position data.'''

import cgi
import json
import os
import yaml


def load_data(data_dir):
    '''Load position data.'''
    data = []
    for filename in os.listdir(data_dir):
        with open(os.path.join(data_dir, filename), 'r') as file_:
            data.append(json.load(file_))
    return data


def get_report(key, data_dir='/var/gps.gmendiola.com'):
    '''Get position report.'''
    gps_key = get_setting('gps_key')
    if key == gps_key:
        return {
            'status': 'ok',
            'data': load_data(data_dir),
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
