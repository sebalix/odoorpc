# -*- coding: utf-8 -*-

from odoorpc.tests import BaseTestCase, session


class TestReqJSON(BaseTestCase):

    def _req_json(self, odoo, url):
        data = odoo.json(
            url,
            {'db': self.env['db'],
             'login': self.env['user'],
             'password': self.env['pwd']})
        self.assertEqual(data['result']['db'], self.env['db'])
        self.assertTrue(data['result']['uid'])
        self.assertEqual(data['result']['username'], self.env['user'])

    @session(login=True)
    def test_req_json_with_leading_slash(self, odoo):
        self._req_json(odoo, '/web/session/authenticate')

    @session(login=True)
    def test_req_json_without_leading_slash(self, odoo):
        self._req_json(odoo, 'web/session/authenticate')
