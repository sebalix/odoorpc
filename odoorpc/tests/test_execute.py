# -*- coding: utf-8 -*-

import numbers
import time

from odoorpc.tests import BaseTestCase, session
import odoorpc


class TestExecute(BaseTestCase):

    # ------
    # Search
    # ------
    @session(login=True)
    def test_execute_search_with_good_args(self, odoo):
        # Check the result returned
        result = odoo.execute('res.users', 'search', [])
        self.assertIsInstance(result, list)
        self.assertIn(odoo.env.user.id, result)
        result = odoo.execute(
            'res.users', 'search', [('id', '=', odoo.env.user.id)])
        self.assertIn(odoo.env.user.id, result)
        self.assertEqual(result[0], odoo.env.user.id)

    @session(login=True)
    def test_execute_search_without_args(self, odoo):
        # Handle exception (execute a 'search' without args)
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.execute,
            'res.users',
            'search')

    @session(login=True)
    def test_execute_search_with_wrong_args(self, odoo):
        # Handle exception (execute a 'search' with wrong args)
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.execute,
            'res.users',
            'search',
            False)  # Wrong arg

    @session(login=True)
    def test_execute_search_with_wrong_model(self, odoo):
        # Handle exception (execute a 'search' with a wrong model)
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.execute,
            'wrong.model',  # Wrong model
            'search',
            [])

    @session(login=True)
    def test_execute_search_with_wrong_method(self, odoo):
        # Handle exception (execute a 'search' with a wrong method)
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.execute,
            'res.users',
            'wrong_method',  # Wrong method
            [])

    # ------
    # Create
    # ------
    @session(login=True)
    def test_execute_create_with_good_args(self, odoo):
        login = "%s_%s" % ("foobar", time.time())
        # Check the result returned
        result = odoo.execute(
            'res.users', 'create',
            {'name': login,
             'login': login})
        self.assertIsInstance(result, numbers.Number)
        # Handle exception (create another user with the same login)
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.execute,
            'res.users', 'create',
            {'name': login, 'login': login})

    @session(login=True)
    def test_execute_create_without_args(self, odoo):
        # Handle exception (execute a 'create' without args)
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.execute,
            'res.users',
            'create')

    @session(login=True)
    def test_execute_create_with_wrong_args(self, odoo):
        # Handle exception (execute a 'create' with wrong args)
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.execute,
            'res.users',
            'create',
            False)  # Wrong arg
