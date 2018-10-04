# -*- coding: utf-8 -*-

import datetime

from odoorpc.tests import BaseTestCase


class TestFieldDate(BaseTestCase):

    def test_field_date_read(self):
        odoo = self.get_session(login=True)
        self.assertIsInstance(odoo.env.user.login_date, datetime.date)

    def test_field_date_write(self):
        odoo = self.get_session(login=True)
        partner = odoo.env.user.company_id.partner_id
        backup = partner.date
        # False
        partner.date = False
        data = partner.read(['date'])[0]
        self.assertEqual(data['date'], False)
        self.assertEqual(partner.date, False)
        # None
        partner.date = None
        data = partner.read(['date'])[0]
        self.assertEqual(data['date'], False)
        self.assertEqual(partner.date, False)
        # 2012-01-01 (string)
        partner.date = '2012-01-01'
        data = partner.read(['date'])[0]
        self.assertEqual(data['date'], '2012-01-01')
        self.assertEqual(partner.date, datetime.date(2012, 1, 1))
        # 2012-01-01 (date object)
        partner.date = datetime.date(2012, 1, 1)
        data = partner.read(['date'])[0]
        self.assertEqual(data['date'], '2012-01-01')
        self.assertEqual(partner.date, datetime.date(2012, 1, 1))
        # Restore original value
        partner.date = backup
        data = partner.read(['date'])[0]
        self.assertEqual(data['date'], backup and backup.strftime('%Y-%m-%d'))
        self.assertEqual(partner.date, backup)
