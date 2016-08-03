#!/usr/bin/env python

'''Logs gps coordinates for beacon.'''

import cgi
import datetime as dt
import json
import yaml
import os


def parse_float(string_):
    '''Parse float from string.'''
    try:
        return float(string_)
    except ValueError:
        return None


def save_data(data):
    '''Save data to beacon working dir.'''
    data_dir = get_setting('gps_dir')
    path = os.path.join(data_dir, '{}.json'.format(data.get('id')))
    if os.path.isfile(path):
        with open(path, 'w') as file_:
            json.dump(data, file_)


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
    tz_offset = -8
    valid_ids = get_setting('valid_ids')
    args = cgi.FieldStorage()
    lat = parse_float(args.getfirst('lat'))
    lon = parse_float(args.getfirst('lon'))
    time = (
        dt.datetime.strptime(args.getfirst('time'), "%Y-%m-%dT%H:%M:%SZ") +
        dt.timedelta(hours=tz_offset)
    )
    speed = parse_float(args.getfirst('s'))
    id_ = args.getfirst('id')

    print 'Content-Type: application/json\n'
    data = {
        'id': id_,
        'lat': lat,
        'lon': lon,
        'time': time.isoformat(),
        'speed': speed,
    }
    if None not in (lat, lon, time, speed, id_) and id_ in valid_ids:
        save_data(data)
        print json.dumps({'status': 'ok'})
    else:
        print json.dumps({'status': 'error', 'data': data})


if __name__ == '__main__':
    main()
