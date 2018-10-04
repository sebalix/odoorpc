# -*- coding: utf-8 -*-

import datetime

from odoorpc.tests import BaseTestCase


class TestFieldDatetime(BaseTestCase):

    def test_field_datetime_read(self):
        odoo = self.get_session(login=True)
        SaleOrder = odoo.env['sale.order']
        order_id = SaleOrder.search([('date_order', '!=', False)], limit=1)
        order = SaleOrder.browse(order_id)
        self.assertIsInstance(order.date_order, datetime.datetime)

    def test_field_datetime_write(self):
        # odoo = self.get_session(login=True)
        # TODO
        # No common model found in every versions of Odoo with a
        # fields.datetime writable
        pass
