# -*- coding: utf-8 -*-

from odoorpc.tests import BaseTestCase


class TestFieldBoolean(BaseTestCase):

    def test_field_boolean_read(self):
        odoo = self.get_session(login=True)
        self.assertTrue(odoo.env.user.active)

    def test_field_boolean_write(self):
        odoo = self.get_session(login=True)
        # TODO: split in several unit tests
        partner = odoo.env.user.partner_id
        backup = partner.customer
        # True
        partner.customer = True
        data = partner.read(['customer'])[0]
        self.assertEqual(data['customer'], True)
        self.assertEqual(partner.customer, True)
        # False
        partner.customer = False
        data = partner.read(['customer'])[0]
        self.assertEqual(data['customer'], False)
        self.assertEqual(partner.customer, False)
        # None
        partner.customer = None
        data = partner.read(['customer'])[0]
        self.assertEqual(data['customer'], False)
        self.assertEqual(partner.customer, False)
        # Restore original value
        partner.customer = backup
        data = partner.read(['customer'])[0]
        self.assertEqual(data['customer'], backup)
        self.assertEqual(partner.customer, backup)
