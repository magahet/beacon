from beacon import service
#import textwrap
from nose.tools import eq_


class TestBeaconService(object):
    #def setUp(self):
        ## Create a temporary directory
        #self.test_dir = tempfile.mkdtemp()
        #settings = textwrap.dedent('''
            #locations_path: {base}/locations.yaml
            #gps_dir: {base}/gps
        #''')

    def test_distance(self):
        beacon_service = service.BeaconService()
        p1 = (40.7127837, -74.00594130000002)
        p2 = (40.71916022743469, -74.17076110839844)
        eq_(beacon_service.distance(p1, p2), 0.0)
