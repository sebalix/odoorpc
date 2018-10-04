# -*- coding: utf-8 -*-

import time

from odoorpc.tests import BaseTestCase
from odoorpc.models import Model
from odoorpc.env import Environment


class TestEnvironment(BaseTestCase):

    def test_env_init(self):
        odoo = self.get_session(login=True)
        self.assertIsInstance(odoo.env, Environment)

    def test_env_context(self):
        odoo = self.get_session(login=True)
        self.assertIn('lang', odoo.env.context)
        self.assertIn('tz', odoo.env.context)
        self.assertIn('uid', odoo.env.context)

    def test_env_lang(self):
        odoo = self.get_session(login=True)
        self.assertEqual(odoo.env.lang, odoo.env.context.get('lang'))

    def test_env_db(self):
        odoo = self.get_session(login=True)
        self.assertEqual(odoo.env.db, self.env['db'])

    def test_env_user(self):
        odoo = self.get_session(login=True)
        self.assertEqual(odoo.env.user.login, self.env['user'])

    def test_env_dirty(self):
        odoo = self.get_session(login=True)
        odoo.config['auto_commit'] = False
        def test_record_garbarge_collected():
            user_ids = odoo.env['res.users'].search([('id', '!=', 1)])
            user = odoo.env['res.users'].browse(user_ids[0])
            self.assertNotIn(user, odoo.env.dirty)
            self.assertNotIn(user, user.env.dirty)
            user.name = "Joe"
            self.assertIn(user, odoo.env.dirty)
            self.assertIn(user, user.env.dirty)
        test_record_garbarge_collected()
        # Ensure the record has been garbage collected for the next test
        import gc
        gc.collect()
        self.assertEqual(list(odoo.env.dirty), [])

    def test_env_registry(self):
        odoo = self.get_session(login=True)
        odoo.env['res.partner']     # pylint: disable=pointless-statement
        self.assertIn('res.partner', odoo.env.registry)
        del odoo.env.registry['res.partner']
        self.assertNotIn('res.partner', odoo.env.registry)
        odoo.env.user.partner_id    # pylint: disable=pointless-statement
        self.assertIn('res.partner', odoo.env.registry)

    def test_env_commit(self):
        # We test with 'auto_commit' deactivated since the commit is implicit
        # by default and sufficiently tested in the 'test_field_*' modules.
        odoo = self.get_session(login=True)
        odoo.config['auto_commit'] = False
        user_id = odoo.env['res.users'].create(
            {'name': "TestCommit", 'login': "test_commit_%s" % time.time()})
        user = odoo.env['res.users'].browse(user_id)
        self.assertNotIn(user, odoo.env.dirty)
        user.name = "Bob"
        self.assertIn(user, odoo.env.dirty)
        odoo.env.commit()
        data = user.read(['name'])[0]
        self.assertEqual(data['name'], "Bob")
        self.assertEqual(user.name, "Bob")
        self.assertNotIn(user, odoo.env.dirty)

    def test_env_ref(self):
        odoo = self.get_session(login=True)
        record = odoo.env.ref('base.lang_en')
        self.assertIsInstance(record, Model)
        self.assertEqual(record._name, 'res.lang')
        self.assertEqual(record.code, 'en_US')

    def test_env_contains(self):
        odoo = self.get_session(login=True)
        self.assertIn('res.partner', odoo.env)
        self.assertNotIn('does.not.exist', odoo.env)
