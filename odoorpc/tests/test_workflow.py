# -*- coding: utf-8 -*-

from odoorpc.tests import BaseTestCase, session
from odoorpc import error, tools


class TestWorkflow(BaseTestCase):

    def setUp(self):
        super(TestWorkflow, self).setUp()
        odoo = self.get_session(login=True)
        self.product_obj = odoo.env['product.product']
        self.partner_obj = odoo.env['res.partner']
        self.sale_order_obj = odoo.env['sale.order']
        self.uom_obj = odoo.env['product.uom']
        self.p_id = self.partner_obj.create({'name': "Child 1"})
        prod_vals = {
            'name': "PRODUCT TEST WORKFLOW",
        }
        self.product_id = self.product_obj.create(prod_vals)
        sol_vals = {
            'name': "TEST WORKFLOW",
            'product_id': self.product_id,
            'product_uom': self.uom_obj.search([])[0],
        }
        so_vals = {
            'partner_id': self.p_id,
            'order_line': [(0, 0, sol_vals)],
        }
        self.so_id = self.sale_order_obj.create(so_vals)

    @session(login=True)
    def test_exec_workflow(self, odoo):
        if tools.v(odoo.version)[0] >= 11:
            self.assertRaises(
                DeprecationWarning,
                odoo.exec_workflow,
                'sale.order', self.so_id, 'order_confirm')
            return
        odoo.exec_workflow('sale.order', self.so_id, 'order_confirm')

    @session(login=True)
    def test_exec_workflow_wrong_model(self, odoo):
        if tools.v(odoo.version)[0] >= 11:
            self.assertRaises(
                DeprecationWarning,
                odoo.exec_workflow,
                'sale.order2', self.so_id, 'order_confirm')
            return
        self.assertRaises(
            error.RPCError,
            odoo.exec_workflow,
            'sale.order2', self.so_id, 'order_confirm')
