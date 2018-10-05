# -*- coding: utf-8 -*-

from odoorpc.tests import BaseTestCase, session


class TestFieldSelection(BaseTestCase):

    @session(login=True)
    def test_field_selection_read(self, odoo):
        self.assertEqual(odoo.env.user.state, 'active')

    @session(login=True)
    def test_field_selection_write(self, odoo):
        # TODO: split in several unit tests
        #record = odoo.env.user
        #data = record.__class__.fields_get()
        #for f in data:
        #    if data[f]['type'] == 'selection':
        #        print("%s" % (f))
        #        #print("%s - %s" % (f, odoo.env.user[f]))
        backup = odoo.env.user.tz
        # False
        odoo.env.user.tz = False
        data = odoo.env.user.read(['tz'])[0]
        self.assertEqual(data['tz'], False)
        self.assertEqual(odoo.env.user.tz, False)
        # None
        odoo.env.user.tz = None
        data = odoo.env.user.read(['tz'])[0]
        self.assertEqual(data['tz'], False)
        self.assertEqual(odoo.env.user.tz, False)
        # Europe/Paris
        odoo.env.user.tz = 'Europe/Paris'
        data = odoo.env.user.read(['tz'])[0]
        self.assertEqual(data['tz'], 'Europe/Paris')
        self.assertEqual(odoo.env.user.tz, 'Europe/Paris')
        # Restore original value
        odoo.env.user.tz = backup
        data = odoo.env.user.read(['tz'])[0]
        self.assertEqual(data['tz'], backup)
        self.assertEqual(odoo.env.user.tz, backup)
