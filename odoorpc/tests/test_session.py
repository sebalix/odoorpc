# -*- coding: utf-8 -*-

import tempfile
import os

from odoorpc.tests import BaseTestCase, session
import odoorpc


class TestSession(BaseTestCase):

    def setUp(self):
        super(TestSession, self).setUp()
        self.session_name = self.env['db']
        self.file_path = tempfile.mkstemp(suffix='.cfg', prefix='odoorpc_')[1]

    def tearDown(self):
        super(TestSession, self).tearDown()
        os.remove(self.file_path)

    def test_session_odoo_list(self):
        result = odoorpc.ODOO.list(rc_file=self.file_path)
        self.assertIsInstance(result, list)
        other_file_path = tempfile.mkstemp()[1]
        result = odoorpc.ODOO.list(rc_file=other_file_path)
        self.assertIsInstance(result, list)

    @session(login=True)
    def test_session_odoo_save_and_remove(self, odoo):
        odoo.save(self.session_name, rc_file=self.file_path)
        result = odoorpc.ODOO.list(rc_file=self.file_path)
        self.assertIn(self.session_name, result)
        odoorpc.ODOO.remove(self.session_name, rc_file=self.file_path)

    @session(login=True)
    def test_session_odoo_load(self, odoo):
        odoo.save(self.session_name, rc_file=self.file_path)
        odoo = odoorpc.ODOO.load(self.session_name, rc_file=self.file_path)
        self.assertIsInstance(odoo, odoorpc.ODOO)
        self.assertEqual(odoo.host, odoo.host)
        self.assertEqual(odoo.port, odoo.port)
        self.assertEqual(odoo.protocol, odoo.protocol)
        self.assertEqual(odoo.env.db, odoo.env.db)
        self.assertEqual(odoo.env.uid, odoo.env.uid)
        odoorpc.ODOO.remove(self.session_name, rc_file=self.file_path)

    @session(login=True)
    def test_session_get(self, odoo):
        odoo.save(self.session_name, rc_file=self.file_path)
        data = {
            'type': odoo.__class__.__name__,
            'host': odoo.host,
            'protocol': odoo.protocol,
            'port': int(odoo.port),
            'timeout': odoo.config['timeout'],
            'user': odoo._login,
            'passwd': odoo._password,
            'database': odoo.env.db,
        }
        result = odoorpc.session.get(
            self.session_name, rc_file=self.file_path)
        self.assertEqual(data, result)
        odoorpc.ODOO.remove(self.session_name, rc_file=self.file_path)

    @session(login=True)
    def test_session_get_all(self, odoo):
        odoo.save(self.session_name, rc_file=self.file_path)
        data = {
            self.session_name: {
                'type': odoo.__class__.__name__,
                'host': odoo.host,
                'protocol': odoo.protocol,
                'port': int(odoo.port),
                'timeout': odoo.config['timeout'],
                'user': odoo._login,
                'passwd': odoo._password,
                'database': odoo.env.db,
            }
        }
        result = odoorpc.session.get_all(rc_file=self.file_path)
        self.assertIn(self.session_name, result)
        self.assertEqual(data, result)
        odoorpc.ODOO.remove(self.session_name, rc_file=self.file_path)
