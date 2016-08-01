#!/usr/bin/env python

import cgi
import cgitb
import datetime as dt
import json
import json
import os
from collections import deque


def parse_float(string_):
    try:
        return float(string_)
    except Exception:
        return None


def save_data(data, data_dir='/var/gps.gmendiola.com/'):
    path = os.path.join(data_dir, '{}.json'.format(data.get('id')))
    with open(path, 'w') as file_:
        json.dump(data, file_)


cgitb.enable()
tz_offset = -8
valid_ids = ('gar', 'jj', 'test', 'ysu')

args = cgi.FieldStorage()
lat = parse_float(args.getfirst('lat'))
lon = parse_float(args.getfirst('lon'))
time = dt.datetime.strptime(args.getfirst('time'), "%Y-%m-%dT%H:%M:%SZ") + dt.timedelta(hours=tz_offset)
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
    print json.dumps({'status': 'incomplete', 'data': data})
