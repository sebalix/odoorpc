# -*- coding: utf-8 -*-

from odoorpc.tests import BaseTestCase, session


class TestFieldBoolean(BaseTestCase):

    @session(login=True)
    def test_field_boolean_read(self, odoo):
        self.assertTrue(odoo.env.user.active)

    @session(login=True)
    def test_field_boolean_write(self, odoo):
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
