# -*- coding: utf-8 -*-

import tempfile

from odoorpc.tests import BaseTestCase
from odoorpc.tools import v


class TestReport(BaseTestCase):

    def test_report_download_pdf(self):
        odoo = self.get_session(login=True)
        model = 'res.company'
        report_name = 'web.preview_internalreport'
        if v(odoo.version)[0] < 11:
            report_name = 'preview.report'
        ids = odoo.env[model].search([])[:20]
        report = odoo.report.download(report_name, ids)
        with tempfile.TemporaryFile(mode='wb', suffix='.pdf') as file_:
            file_.write(report.read())

    def test_report_download_qweb_pdf(self):
        odoo = self.get_session(login=True)
        model = 'account.invoice'
        report_name = 'account.report_invoice'
        ids = odoo.env[model].search([])[:10]
        report = odoo.report.download(report_name, ids)
        with tempfile.TemporaryFile(mode='wb', suffix='.pdf') as file_:
            file_.write(report.read())

    def test_report_download_wrong_report_name(self):
        odoo = self.get_session(login=True)
        self.assertRaises(
            ValueError,
            odoo.report.download, 'wrong_report', [1])

    def test_report_list(self):
        odoo = self.get_session(login=True)
        res = odoo.report.list()
        self.assertIsInstance(res, dict)
        self.assertIn('account.invoice', res)
        self.assertTrue(
            any('account.report_invoice' in data['report_name']
                for data in res['account.invoice']))
