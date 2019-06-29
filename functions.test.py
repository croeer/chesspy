# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 21:45:00 2019

@author: croeer
"""

import unittest
from functions import *

class FunctionsTest(unittest.TestCase):
    def test_reverseFen_1(self):
        fen = '5k2/4rpbQ/pq4p1/3p2P1/2pP1BP1/2P2PK1/P7/4R3'
        fen_reverse = reverse_fen(fen)
        self.assertEqual(fen_reverse, '3r4/7p/1kp2p2/1pb1pP2/1p2P3/1P4QP/qBPR4/2K5')

    def test_reverseFen_2(self):
        fen = '8/8/8/8/8/8/8/8'
        fen_reverse = reverse_fen(fen)
        self.assertEqual(fen_reverse, fen)

if __name__ == '__main__':
    unittest.main()