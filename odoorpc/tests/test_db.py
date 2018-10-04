# -*- coding: utf-8 -*-

from datetime import datetime
import zipfile

from odoorpc.tests import BaseTestCase
import odoorpc


class TestDB(BaseTestCase):

    def test_db_dump(self):
        odoo = self.get_session()
        dump = odoo.db.dump(self.env['super_pwd'], self.env['db'])
        self.assertIn('dump.sql', zipfile.ZipFile(dump).namelist())

    def test_db_dump_wrong_database(self):
        odoo = self.get_session()
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.db.dump, self.env['super_pwd'], 'wrong_db')

    def test_db_dump_wrong_password(self):
        odoo = self.get_session()
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.db.dump, 'wrong_password', self.env['db'])

    def test_db_create(self):
        odoo = self.get_session()
        date = datetime.strftime(datetime.today(), '%Y%m%d_%Hh%Mm%S')
        new_database = "%s_%s" % (self.env['db'], date)
        odoo.db.create(self.env['super_pwd'], new_database)
        self._drop_db(odoo, new_database)

    def test_db_create_existing_database(self):
        odoo = self.get_session()
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.db.create, self.env['super_pwd'], self.env['db'])

    def test_db_create_wrong_password(self):
        odoo = self.get_session()
        date = datetime.strftime(datetime.today(), '%Y%m%d_%Hh%Mm%S')
        new_database = "%s_%s" % (self.env['db'], date)
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.db.create, 'wrong_password', new_database)
        self._drop_db(odoo, new_database)

    def test_db_drop(self):
        odoo = self.get_session()
        date = datetime.strftime(datetime.today(), '%Y%m%d_%Hh%Mm%S')
        new_database = "%s_%s" % (self.env['db'], date)
        odoo.db.duplicate(
            self.env['super_pwd'], self.env['db'], new_database)
        res = odoo.db.drop(self.env['super_pwd'], new_database)
        self.assertTrue(res)
        self._drop_db(odoo, new_database)

    def test_db_drop_wrong_database(self):
        odoo = self.get_session()
        res = odoo.db.drop(self.env['super_pwd'], 'wrong_database')
        self.assertFalse(res)

    def test_db_drop_wrong_password(self):
        odoo = self.get_session()
        date = datetime.strftime(datetime.today(), '%Y%m%d_%Hh%Mm%S')
        new_database = "%s_%s" % (self.env['db'], date)
        odoo.db.duplicate(
            self.env['super_pwd'], self.env['db'], new_database)
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.db.drop, 'wrong_password', new_database)
        self._drop_db(odoo, new_database)

    def test_db_duplicate(self):
        odoo = self.get_session()
        date = datetime.strftime(datetime.today(), '%Y%m%d_%Hh%Mm%S')
        new_database = "%s_%s" % (self.env['db'], date)
        odoo.db.duplicate(
            self.env['super_pwd'], self.env['db'], new_database)
        self._drop_db(odoo, new_database)

    def test_db_duplicate_wrong_database(self):
        odoo = self.get_session()
        date = datetime.strftime(datetime.today(), '%Y%m%d_%Hh%Mm%S')
        new_database = "%s_%s" % (self.env['db'], date)
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.db.duplicate,
            self.env['super_pwd'], 'wrong_database', new_database)
        self._drop_db(odoo, new_database)

    def test_db_duplicate_wrong_password(self):
        odoo = self.get_session()
        date = datetime.strftime(datetime.today(), '%Y%m%d_%Hh%Mm%S')
        new_database = "%s_%s" % (self.env['db'], date)
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.db.duplicate,
            'wrong_password', self.env['db'], new_database)
        self._drop_db(odoo, new_database)

    def test_db_list(self):
        odoo = self.get_session()
        res = odoo.db.list()
        self.assertIsInstance(res, list)
        self.assertIn(self.env['db'], res)

    def test_db_restore_new_database(self):
        odoo = self.get_session()
        dump = odoo.db.dump(self.env['super_pwd'], self.env['db'])
        date = datetime.strftime(datetime.today(), '%Y-%m-%d_%Hh%Mm%S')
        new_database = "%s_%s" % (self.env['db'], date)
        odoo.db.restore(
            self.env['super_pwd'], new_database, dump)
        self._drop_db(odoo, new_database)

    def test_db_restore_existing_database(self):
        odoo = self.get_session()
        dump = odoo.db.dump(self.env['super_pwd'], self.env['db'])
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.db.restore,
            self.env['super_pwd'], self.env['db'], dump)
        self._drop_db(odoo, self.env['db'])

    def test_db_restore_wrong_password(self):
        odoo = self.get_session()
        dump = odoo.db.dump(self.env['super_pwd'], self.env['db'])
        date = datetime.strftime(datetime.today(), '%Y%m%d_%Hh%Mm%S')
        new_database = "%s_%s" % (self.env['db'], date)
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.db.restore,
            'wrong_password', new_database, dump)
        self._drop_db(odoo, new_database)
