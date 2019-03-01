# -*- coding: UTF-8 -*-
try:
    import unittest2 as unittest
except:
    import unittest

import os

import odoorpc


class BaseTestCase(unittest.TestCase):
    """Instanciates an ``odoorpc.ODOO`` object, nothing more."""
    @classmethod
    def setUpClass(cls):
        super(BaseTestCase, cls).setUpClass()
        try:
            port = int(os.environ.get('ORPC_TEST_PORT', 8069))
        except ValueError:
            raise ValueError("The port must be an integer")
        cls.env = {
            'protocol': os.environ.get('ORPC_TEST_PROTOCOL', 'jsonrpc'),
            'host': os.environ.get('ORPC_TEST_HOST', 'localhost'),
            'port': port,
            'db': os.environ.get('ORPC_TEST_DB', 'odoorpc_test'),
            'user': os.environ.get('ORPC_TEST_USER', 'admin'),
            'pwd': os.environ.get('ORPC_TEST_PWD', 'admin'),
            'version': os.environ.get('ORPC_TEST_VERSION', None),
            'super_pwd': os.environ.get('ORPC_TEST_SUPER_PWD', 'admin'),
        }
        cls.odoo = odoorpc.ODOO(
            cls.env['host'], protocol=cls.env['protocol'],
            port=cls.env['port'], version=cls.env['version'])
        # Create the database
        default_timeout = cls.odoo.config['timeout']
        cls.odoo.config['timeout'] = 600
        if cls.env['db'] not in cls.odoo.db.list():
            cls.odoo.db.create(
                cls.env['super_pwd'], cls.env['db'], True)
        cls.odoo.config['timeout'] = default_timeout


class LoginTestCase(BaseTestCase):
    """Instanciates an ``odoorpc.ODOO`` object and perform the user login."""
    @classmethod
    def setUpClass(cls):
        super(LoginTestCase, cls).setUpClass()
        default_timeout = cls.odoo.config['timeout']
        cls.odoo.login(cls.env['db'], cls.env['user'], cls.env['pwd'])
        # Install 'sale' + 'crm_claim' on Odoo < 10.0,
        # and 'sale' + 'subscription' on Odoo >= 10.0
        cls.odoo.config['timeout'] = 600
        module_obj = cls.odoo.env['ir.module.module']
        modules = ['sale', 'crm_claim']
        if cls.odoo.version == '10.0':
            modules = ['sale', 'subscription']
        module_ids = module_obj.search([('name', 'in', modules)])
        module_obj.button_immediate_install(module_ids)
        cls.odoo.config['timeout'] = default_timeout
        # Get user record and model after the installation of modules
        # to get all available fields (avoiding test failures)
        cls.user = cls.odoo.env.user
        cls.user_obj = cls.odoo.env['res.users']

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
