# -*- coding: utf-8 -*-

from odoorpc.tests import BaseTestCase, session


class TestFieldChar(BaseTestCase):

    @session(login=True)
    def test_field_char_read(self, odoo):
        self.assertEqual(odoo.env.user.login, self.env['user'])

    @session(login=True)
    def test_field_char_write(self, odoo):
        # TODO: split in several unit tests
        partner = odoo.env.user.partner_id
        backup = partner.street
        # "A street"
        partner.street = "A street"
        data = partner.read(['street'])[0]
        self.assertEqual(data['street'], "A street")
        self.assertEqual(partner.street, "A street")
        # False
        partner.street = False
        data = partner.read(['street'])[0]
        self.assertEqual(data['street'], False)
        self.assertEqual(partner.street, False)
        # None
        partner.street = None
        data = partner.read(['street'])[0]
        self.assertEqual(data['street'], False)
        self.assertEqual(partner.street, False)
        # Restore original value
        partner.street = backup
        data = partner.read(['street'])[0]
        self.assertEqual(data['street'], backup)
        self.assertEqual(partner.street, backup)
