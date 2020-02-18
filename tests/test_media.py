""" Test media """

import unittest
from media_mover.mover import demangle_showname


##############################################################################
class test_demangle(unittest.TestCase):
    """ Test demangling """
    TESTS = [
        [
            'Star.Wars.The.Clone.Wars.S03E19.1080p.BluRay',
            ('Star Wars The Clone Wars', None, 3, 19)
        ],
        [
            'Doctor.Who.2005.S12E05.720p.x265-ZMNT',
            ('Doctor Who', '2005', 12, 5)
        ],
        [
            '_UNPACK_Succession.S01E08.Prague.1080p',
            ('Succession', None, 1, 8)
        ],
        [
            'Nomatch',
            (None, None, None, None)
        ]
    ]

    def test_dem(self):
        """ Test demangling """
        for test in self.TESTS:
            ans = demangle_showname(test[0])
            self.assertEqual(ans, test[1])
