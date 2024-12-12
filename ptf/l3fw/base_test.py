"""
Base classes for test cases.
Create test importing this class for each test items.
"""

import ptf
from ptf.base_tests import BaseTest
import ptf.testutils as testutils

# TODO: Add class to connect to and configure DUT(switch)

class DutTest(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)

        test_params = testutils.test_params_get()
        print()
        if test_params.items():
            print("You specified the following test-params when invoking ptf:")
            for k, v in list(test_params.items()):
                print(k, ":\t\t\t", v)
        
        #dataplane
        self.dataplane = ptf.dataplane_instance
        self.dataplane.flush()

    def tearDown(self):
        BaseTest.tearDown(self)
