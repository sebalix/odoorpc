# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except:
    import unittest

import odoorpc


class TestShell(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.shell = odoorpc.shell.Shell()

    def test_locals(self):
        self.assertEqual(self.shell.locals['odoorpc'], odoorpc)
        self.assertEqual(self.shell.locals['ODOO'], odoorpc.ODOO)
