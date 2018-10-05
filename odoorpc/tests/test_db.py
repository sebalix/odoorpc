# -*- coding: utf-8 -*-

from datetime import datetime
import zipfile

from odoorpc.tests import BaseTestCase, session
import odoorpc


def get_new_dbname(obj, fmt='%Y%m%d_%Hh%Mm%S'):
    date = datetime.strftime(datetime.today(), fmt)
    return "%s_%s" % (obj.env['db'], date)


class TestDB(BaseTestCase):

    @session()
    def test_db_dump(self, odoo):
        dump = odoo.db.dump(self.env['super_pwd'], self.env['db'])
        self.assertIn('dump.sql', zipfile.ZipFile(dump).namelist())

    @session()
    def test_db_dump_wrong_database(self, odoo):
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.db.dump, self.env['super_pwd'], 'wrong_db')

    @session()
    def test_db_dump_wrong_password(self, odoo):
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.db.dump, 'wrong_password', self.env['db'])

    @session()
    def test_db_create(self, odoo):
        new_database = get_new_dbname(self)
        odoo.db.create(self.env['super_pwd'], new_database)
        self._drop_db(odoo, new_database)

    @session()
    def test_db_create_existing_database(self, odoo):
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.db.create, self.env['super_pwd'], self.env['db'])

    @session()
    def test_db_create_wrong_password(self, odoo):
        new_database = get_new_dbname(self)
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.db.create, 'wrong_password', new_database)
        self._drop_db(odoo, new_database)

    @session()
    def test_db_drop(self, odoo):
        new_database = get_new_dbname(self)
        odoo.db.duplicate(
            self.env['super_pwd'], self.env['db'], new_database)
        res = odoo.db.drop(self.env['super_pwd'], new_database)
        self.assertTrue(res)
        self._drop_db(odoo, new_database)

    @session()
    def test_db_drop_wrong_database(self, odoo):
        res = odoo.db.drop(self.env['super_pwd'], 'wrong_database')
        self.assertFalse(res)

    @session()
    def test_db_drop_wrong_password(self, odoo):
        new_database = get_new_dbname(self)
        odoo.db.duplicate(
            self.env['super_pwd'], self.env['db'], new_database)
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.db.drop, 'wrong_password', new_database)
        self._drop_db(odoo, new_database)

    @session()
    def test_db_duplicate(self, odoo):
        new_database = get_new_dbname(self)
        odoo.db.duplicate(
            self.env['super_pwd'], self.env['db'], new_database)
        self._drop_db(odoo, new_database)

    @session()
    def test_db_duplicate_wrong_database(self, odoo):
        new_database = get_new_dbname(self)
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.db.duplicate,
            self.env['super_pwd'], 'wrong_database', new_database)
        self._drop_db(odoo, new_database)

    @session()
    def test_db_duplicate_wrong_password(self, odoo):
        new_database = get_new_dbname(self)
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.db.duplicate,
            'wrong_password', self.env['db'], new_database)
        self._drop_db(odoo, new_database)

    @session()
    def test_db_list(self, odoo):
        res = odoo.db.list()
        self.assertIsInstance(res, list)
        self.assertIn(self.env['db'], res)

    @session()
    def test_db_restore_new_database(self, odoo):
        dump = odoo.db.dump(self.env['super_pwd'], self.env['db'])
        new_database = get_new_dbname(self, fmt='%Y-%m-%d_%Hh%Mm%S')
        odoo.db.restore(self.env['super_pwd'], new_database, dump)
        self._drop_db(odoo, new_database)

    @session()
    def test_db_restore_existing_database(self, odoo):
        dump = odoo.db.dump(self.env['super_pwd'], self.env['db'])
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.db.restore,
            self.env['super_pwd'], self.env['db'], dump)

    @session()
    def test_db_restore_wrong_password(self, odoo):
        dump = odoo.db.dump(self.env['super_pwd'], self.env['db'])
        new_database = get_new_dbname(self)
        self.assertRaises(
            odoorpc.error.RPCError,
            odoo.db.restore,
            'wrong_password', new_database, dump)
        self._drop_db(odoo, new_database)
