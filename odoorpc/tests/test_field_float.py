# -*- coding: utf-8 -*-

from odoorpc.tests import BaseTestCase


class TestFieldFloat(BaseTestCase):

    def test_field_float_read(self):
        odoo = self.get_session(login=True)
        self.assertEqual(odoo.env.user.credit_limit, 0.0)

    def test_field_float_write(self):
        odoo = self.get_session(login=True)
        # TODO: split in several unit tests
        partner = odoo.env.user.partner_id
        backup = partner.credit_limit
        # False
        partner.credit_limit = False
        data = partner.read(['credit_limit'])[0]
        self.assertEqual(data['credit_limit'], 0.0)
        self.assertEqual(partner.credit_limit, 0.0)
        # None
        partner.credit_limit = None
        data = partner.read(['credit_limit'])[0]
        self.assertEqual(data['credit_limit'], 0.0)
        self.assertEqual(partner.credit_limit, 0.0)
        # 0.0
        partner.credit_limit = 0.0
        data = partner.read(['credit_limit'])[0]
        self.assertEqual(data['credit_limit'], 0.0)
        self.assertEqual(partner.credit_limit, 0.0)
        # 100.0
        partner.credit_limit = 100.0
        data = partner.read(['credit_limit'])[0]
        self.assertEqual(data['credit_limit'], 100.0)
        self.assertEqual(partner.credit_limit, 100.0)
        # Restore original value
        partner.credit_limit = backup
        data = partner.read(['credit_limit'])[0]
        self.assertEqual(data['credit_limit'], backup)
        self.assertEqual(partner.credit_limit, backup)
