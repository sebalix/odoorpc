# -*- coding: utf-8 -*-
from functools import wraps
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import os

import odoorpc

try:
    port = int(os.environ.get('ORPC_TEST_PORT', 8069))
except ValueError:
    raise ValueError("The port must be an integer")
ENV = {
    'protocol': os.environ.get('ORPC_TEST_PROTOCOL', 'jsonrpc'),
    'host': os.environ.get('ORPC_TEST_HOST', 'localhost'),
    'port': port,
    'db': os.environ.get('ORPC_TEST_DB', 'odoorpc_test'),
    'user': os.environ.get('ORPC_TEST_USER', 'admin'),
    'pwd': os.environ.get('ORPC_TEST_PWD', 'admin'),
    'version': os.environ.get('ORPC_TEST_VERSION', None),
    'super_pwd': os.environ.get('ORPC_TEST_SUPER_PWD', 'admin'),
}


class BaseTestCase(unittest.TestCase):
    """Base class to implement tests. It will create automatically
    an Odoo database and install some modules in order to perform
    integration tests.
    """
    db_created = False
    modules_installed = False

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.env = dict(ENV)

    @classmethod
    def get_session(cls, login=False):
        odoo = odoorpc.ODOO(
            ENV['host'], protocol=ENV['protocol'],
            port=ENV['port'], version=ENV['version'])
        if login:
            odoo.login(ENV['db'], ENV['user'], ENV['pwd'])
        return odoo

    @classmethod
    def _create_db(cls, dbname):
        """Create the database `dbname` if it does not exist."""
        if cls.db_created:
            return
        odoo = cls.get_session()
        default_timeout = odoo.config['timeout']
        odoo.config['timeout'] = 600
        if dbname not in odoo.db.list():
            odoo.db.create(ENV['super_pwd'], dbname, True)
        odoo.config['timeout'] = default_timeout
        cls.db_created = True

    @classmethod
    def _drop_db(cls, odoo, dbname):
        """Drop the database `dbname`."""
        try:
            odoo.db.drop(ENV['super_pwd'], dbname)
        except:     # pylint: disable=bare-except,except-pass
            pass

    @classmethod
    def _install_modules(cls):
        if cls.modules_installed:
            return
        odoo = cls.get_session(login=True)
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
        cls.modules_installed = True


def session(login=False):
    def decorated(func):
        BaseTestCase._create_db(ENV['db'])
        BaseTestCase._install_modules()
        odoo = BaseTestCase.get_session(login)
        @wraps(func)
        def wrapper(*args, **kwargs):
            kwargs['odoo'] = odoo
            return func(*args, **kwargs)
        return wrapper
    return decorated
