#!/usr/bin/env python

'''Runner for beacon app'''

import beacon
import logging


def main():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(message)s',
        '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    beacon_service = beacon.BeaconService()
    try:
        beacon_service.run()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
