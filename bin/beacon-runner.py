#!/usr/bin/env python

'''Runner for beacon app'''

import logging
import argparse
import beacon


def main():
    parser = argparse.ArgumentParser(description='Beacon location tracker')
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    args = parser.parse_args()
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(message)s',
        '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    beacon_service = beacon.BeaconService()
    try:
        beacon_service.run()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
