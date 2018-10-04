# -*- coding: utf-8 -*-

import socket

from odoorpc.tests import BaseTestCase
from odoorpc.tools import v


class TestTimeout(BaseTestCase):

    def test_increased_timeout(self):
        odoo = self.get_session(login=True)
        # Set the timeout
        odoo.config['timeout'] = 120
        # Execute a time consuming query: no exception
        report_name = 'web.preview_internalreport'
        if v(odoo.version)[0] < 11:
            report_name = 'preview.report'
        odoo.report.download(report_name, [1])

    def test_reduced_timeout(self):
        odoo = self.get_session(login=True)
        # Set the timeout
        odoo.config['timeout'] = 0.005
        # Execute a time consuming query: handle exception
        report_name = 'web.preview_internalreport'
        if v(odoo.version)[0] < 11:
            report_name = 'preview.report'
        self.assertRaises(
            socket.timeout,
            odoo.report.download, report_name, [1])
