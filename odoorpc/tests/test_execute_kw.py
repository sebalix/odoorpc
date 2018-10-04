# -*- coding: utf-8 -*-

import numbers
import time

from odoorpc.tests import BaseTestCase
import odoorpc


class TestExecuteKw(BaseTestCase):

    # ------
    # Search
    # ------
    def test_execute_kw_search_with_good_args(self):
        odoo = self.get_session(login=True)
        # Check the result returned
        result = odoo.execute_kw('res.users', 'search', [[]], {})
        self.assertIsInstance(result, list)
        self.assertIn(odoo.env.user.id, result)
        result = odoo.execute_kw(
            'res.users', 'search',
            [[('id', '=', odoo.env.user.id)]], {'order': 'name'})
        self.assertIn(odoo.env.user.id, result)
        self.assertEqual(result[0], odoo.env.user.id)

    def test_execute_kw_search_without_args(self):
        odoo = self.get_session(login=True)
        # Handle exception (execute a 'search' without args)
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.execute_kw,
            'res.users',
            'search')

    def test_execute_kw_search_with_wrong_args(self):
        odoo = self.get_session(login=True)
        # Handle exception (execute a 'search' with wrong args)
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.execute_kw,
            'res.users',
            'search',
            False, False)   # Wrong args

    def test_execute_kw_search_with_wrong_model(self):
        odoo = self.get_session(login=True)
        # Handle exception (execute a 'search' with a wrong model)
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.execute_kw,
            'wrong.model',  # Wrong model
            'search',
            [[]], {})

    def test_execute_kw_search_with_wrong_method(self):
        odoo = self.get_session(login=True)
        # Handle exception (execute a 'search' with a wrong method)
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.execute_kw,
            'res.users',
            'wrong_method',  # Wrong method
            [[]], {})

    # ------
    # Create
    # ------
    def test_execute_kw_create_with_good_args(self):
        odoo = self.get_session(login=True)
        login = "%s_%s" % ("foobar", time.time())
        # Check the result returned
        result = odoo.execute_kw(
            'res.users', 'create',
            [{'name': login, 'login': login}])
        self.assertIsInstance(result, numbers.Number)
        # Handle exception (create another user with the same login)
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.execute_kw,
            'res.users', 'create',
            [{'name': login, 'login': login}])

    def test_execute_kw_create_without_args(self):
        odoo = self.get_session(login=True)
        # Handle exception (execute a 'create' without args)
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.execute_kw,
            'res.users',
            'create')

    def test_execute_kw_create_with_wrong_args(self):
        odoo = self.get_session(login=True)
        # Handle exception (execute a 'create' with wrong args)
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.execute_kw,
            'res.users',
            'create',
            True, True)   # Wrong args
