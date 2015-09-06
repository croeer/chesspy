# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 20:53:59 2015

@author: croeer
"""

import unittest
from functions import *

def fun(x):
    return x + 1

class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(fun(3), 4)
        
if __name__ == '__main__':
    unittest.main()