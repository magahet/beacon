BEACON
=======

This is a simple webapp to log the position of individuals with an appropriate smartphone app, and allow users to write notification rules to alert them on changes in position, speed, etc.

An example use case is to notify user A when user B leaves the office for the day.


## Currently implemented features

### /etc/beacon/locations.yaml

This file specifies a list of places to watch for individuals entering and leaving. The format is below:

    -
        name: location1
        lat: 34.23423
        lon: -118.39433
        radius: 10 # in meters
        email: user@domain.com
    -
        name: location2
        lat: 34.23423
        lon: -118.39433
        radius: 20
        email: user@domain.com, user2@domain.com


## Deployment

There's a makefile that runs ansible to deploy code. Settings will need to be created manually from there. A example settings.yaml file is deployed to /etc/beacon/.

Ansible requires a env.yml file with the following:

    [ec2]
    <fqdn for server>

    [ec2:vars]
    fqdn=<fqdn for server>
