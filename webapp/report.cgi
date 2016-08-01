#!/usr/bin/env python

import cgi
import cgitb
import json
import os


cgitb.enable()


def load_data(data_dir):
    data = []
    for filename in os.listdir(data_dir):
        with open(os.path.join(data_dir, filename), 'r') as file_:
            data.append(json.load(file_))
    return data


def get_report(key, data_dir='/var/gps.gmendiola.com'):
    if key == os.getenv('GPSKEY', ''):
        return {
            'status': 'ok',
            'data': load_data(data_dir),
        }
    else:
        return {'status': 'unauthorized'}


if __name__ == '__main__':
    args = cgi.FieldStorage()
    key = args.getfirst('key', '')
    print 'Content-Type: application/json\n'
    print json.dumps(get_report(key), indent=2)
