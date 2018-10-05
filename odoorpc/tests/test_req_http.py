# -*- coding: utf-8 -*-

from odoorpc.tests import BaseTestCase, session


class TestReqHTTP(BaseTestCase):

    def _req_http(self, odoo, url):
        response = odoo.http(url)
        binary_data = response.read()
        self.assertTrue(binary_data)

    @session(login=True)
    def test_req_http_with_leading_slash(self, odoo):
        self._req_http(odoo, '/web/binary/company_logo')

    @session(login=True)
    def test_req_http_without_leading_slash(self, odoo):
        self._req_http(odoo, 'web/binary/company_logo')
