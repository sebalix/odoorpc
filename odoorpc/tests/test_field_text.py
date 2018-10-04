# -*- coding: utf-8 -*-

import sys

from odoorpc.tests import BaseTestCase

# Python 2
if sys.version_info.major < 3:
    def is_string(arg):
        return isinstance(arg, (str, unicode))
# Python >= 3
else:
    def is_string(arg):
        return isinstance(arg, str)


class TestFieldText(BaseTestCase):

    def test_field_text_read(self):
        odoo = self.get_session(login=True)
        # Test empty field
        self.assertFalse(odoo.env.user.comment)
        # Test field containing a value
        Module = odoo.env['ir.module.module']
        sale_id = Module.search([('name', '=', 'sale')])
        sale_mod = Module.browse(sale_id)
        self.assertTrue(is_string(sale_mod.views_by_module))

    def test_field_text_write(self):
        # TODO
        pass
