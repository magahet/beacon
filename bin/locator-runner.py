#!/usr/bin/env python

'''Runner for locator app'''

import locator
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
    locator_service = locator.LocationService()
    try:
        locator_service.run()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
