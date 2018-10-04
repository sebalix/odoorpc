# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import os

import odoorpc


class BaseTestCase(unittest.TestCase):
    """Instanciates an ``odoorpc.ODOO`` object, nothing more."""
    def __new__(cls, *args, **kwargs):
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
        super_new = super(BaseTestCase, cls).__new__
        if super_new is object.__new__:
            return super_new(cls)
        return super_new(cls, *args, **kwargs)

    def setUp(self):
        super(BaseTestCase, self).setUp()
        odoo = self.get_session()
        self._create_db(odoo, self.env['db'])
        odoo = self.get_session(login=True)
        self._install_modules(odoo)

    @classmethod
    def get_session(cls, login=False):
        odoo = odoorpc.ODOO(
            cls.env['host'], protocol=cls.env['protocol'],
            port=cls.env['port'], version=cls.env['version'])
        if login:
            odoo.login(cls.env['db'], cls.env['user'], cls.env['pwd'])
        return odoo

    @classmethod
    def _create_db(cls, odoo, dbname):
        """Create the database `dbname` if it does not exist."""
        default_timeout = odoo.config['timeout']
        odoo.config['timeout'] = 600
        if dbname not in odoo.db.list():
            odoo.db.create(cls.env['super_pwd'], dbname, True)
        odoo.config['timeout'] = default_timeout

    @classmethod
    def _drop_db(cls, odoo, dbname):
        """Drop the database `dbname`."""
        try:
            odoo.db.drop(cls.env['super_pwd'], dbname)
        except:     # pylint: disable=bare-except,except-pass
            pass

    @classmethod
    def _install_modules(cls, odoo):
        default_timeout = odoo.config['timeout']
        # Install 'sale' + 'crm_claim' on Odoo < 10.0,
        # and 'sale' + 'subscription' on Odoo >= 10.0
        odoo.config['timeout'] = 600
        module_obj = odoo.env['ir.module.module']
        modules = ['sale', 'crm_claim']
        if odoo.version == '10.0':
            modules = ['sale', 'subscription']
        module_ids = module_obj.search([
            ('name', 'in', modules),
            ('state', 'in', ('uninstalled', 'to install', 'to remove')),
        ])
        if module_ids:
            module_obj.button_immediate_install(module_ids)
        odoo.config['timeout'] = default_timeout
        # Get user record and model after the installation of modules
        # to get all available fields (avoiding test failures)
        # FIXME: is it still relevant?
        # user = odoo.env.user
        # user_obj = odoo.env['res.users']
