# -*- coding: utf-8 -*-

from odoorpc.tests import BaseTestCase, session


class TestFieldInteger(BaseTestCase):

    @session(login=True)
    def test_field_integer_read(self, odoo):
        self.assertIsInstance(odoo.env.user.id, int)

    @session(login=True)
    def test_field_integer_write(self, odoo):
        cron_obj = odoo.env['ir.cron']
        cron = cron_obj.browse(cron_obj.search([])[0])
        backup = cron.priority
        # False
        cron.priority = False
        data = cron.read(['priority'])[0]
        self.assertEqual(data['priority'], 0)
        self.assertEqual(cron.priority, 0)
        # None
        cron.priority = None
        data = cron.read(['priority'])[0]
        self.assertEqual(data['priority'], 0)
        self.assertEqual(cron.priority, 0)
        # 0
        cron.priority = 0
        data = cron.read(['priority'])[0]
        self.assertEqual(data['priority'], 0)
        self.assertEqual(cron.priority, 0)
        # 100
        cron.priority = 100
        data = cron.read(['priority'])[0]
        self.assertEqual(data['priority'], 100)
        self.assertEqual(cron.priority, 100)
        # Restore original value
        cron.priority = backup
        data = cron.read(['priority'])[0]
        self.assertEqual(data['priority'], backup)
        self.assertEqual(cron.priority, backup)
