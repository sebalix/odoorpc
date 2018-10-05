# -*- coding: utf-8 -*-

import time

from odoorpc.tests import BaseTestCase, session
from odoorpc.models import Model


class TestFieldMany2many(BaseTestCase):

    def _generate_data(self, odoo):
        u0_id = odoo.env['res.users'].create({
            'name': "TestMany2many User 1",
            'login': 'test_m2m_u1_%s' % time.time(),
        })
        g1_id = odoo.env['res.groups'].create({'name': "Group 1"})
        g2_id = odoo.env['res.groups'].create({'name': "Group 2"})
        u1_id = odoo.env['res.users'].create({
            'name': "TestMany2many User 2",
            'login': 'test_m2m_u2_%s' % time.time(),
            'groups_id': [(4, g1_id), (4, g2_id)],
        })
        return {
            'u0_id': u0_id,
            'g1_id': g1_id,
            'g2_id': g2_id,
            'u1_id': u1_id,
        }

    @session(login=True)
    def test_field_many2many_read(self, odoo):
        self.assertIsInstance(odoo.env.user.company_ids, Model)
        self.assertEqual(odoo.env.user.company_ids._name, 'res.company')
        # Test if empty field returns an empty recordset, and not False
        self.assertIsInstance(odoo.env.user.message_follower_ids, Model)
        self.assertEqual(odoo.env.user.message_follower_ids.ids, [])
        self.assertFalse(bool(odoo.env.user.message_follower_ids))

    @session(login=True)
    def test_field_many2many_write_set_false(self, odoo):
        d = self._generate_data(odoo)
        user = odoo.env['res.users'].browse(d['u0_id'])
        # False
        user.groups_id = False
        data = user.read(['groups_id'])[0]
        self.assertEqual(data['groups_id'], [])
        self.assertEqual(list(user.groups_id), [])

    @session(login=True)
    def test_field_many2many_write_set_empty_list(self, odoo):
        d = self._generate_data(odoo)
        user = odoo.env['res.users'].browse(d['u0_id'])
        # = []
        user.groups_id = []
        data = user.read(['groups_id'])[0]
        self.assertEqual(data['groups_id'], [])
        self.assertEqual(list(user.groups_id), [])

    @session(login=True)
    def test_field_many2many_write_set_magic_tuples(self, odoo):
        d = self._generate_data(odoo)
        user = odoo.env['res.users'].browse(d['u0_id'])
        # [(6, 0, IDS)]
        user.groups_id = [(6, 0, [d['g1_id'], d['g2_id']])]
        data = user.read(['groups_id'])[0]
        self.assertIn(d['g1_id'], data['groups_id'])
        self.assertIn(d['g2_id'], data['groups_id'])
        self.assertEqual(len(data['groups_id']), 2)
        group_ids = [grp.id for grp in user.groups_id]
        self.assertIn(d['g1_id'], group_ids)
        self.assertIn(d['g2_id'], group_ids)
        self.assertEqual(len(group_ids), 2)

    @session(login=True)
    def test_field_many2many_write_iadd_id(self, odoo):
        d = self._generate_data(odoo)
        user = odoo.env['res.users'].browse(d['u0_id'])
        # += ID
        user.groups_id += d['g1_id']
        user.groups_id += d['g2_id']
        data = user.read(['groups_id'])[0]
        self.assertIn(d['g1_id'], data['groups_id'])
        self.assertIn(d['g2_id'], data['groups_id'])
        group_ids = [grp.id for grp in user.groups_id]
        self.assertIn(d['g1_id'], group_ids)
        self.assertIn(d['g2_id'], group_ids)

    @session(login=True)
    def test_field_many2many_write_iadd_record(self, odoo):
        d = self._generate_data(odoo)
        user = odoo.env['res.users'].browse(d['u0_id'])
        # += Record
        user.groups_id += odoo.env['res.groups'].browse(d['g2_id'])
        data = user.read(['groups_id'])[0]
        self.assertNotIn(d['g1_id'], data['groups_id'])
        self.assertIn(d['g2_id'], data['groups_id'])
        group_ids = [grp.id for grp in user.groups_id]
        self.assertNotIn(d['g1_id'], group_ids)
        self.assertIn(d['g2_id'], group_ids)

    @session(login=True)
    def test_field_many2many_write_iadd_recordset(self, odoo):
        d = self._generate_data(odoo)
        user = odoo.env['res.users'].browse(d['u0_id'])
        # += Recordset
        user.groups_id += odoo.env['res.groups'].browse(
            [d['g1_id'], d['g2_id']])
        data = user.read(['groups_id'])[0]
        self.assertIn(d['g1_id'], data['groups_id'])
        self.assertIn(d['g2_id'], data['groups_id'])
        group_ids = [grp.id for grp in user.groups_id]
        self.assertIn(d['g1_id'], group_ids)
        self.assertIn(d['g2_id'], group_ids)

    @session(login=True)
    def test_field_many2many_write_iadd_list_ids(self, odoo):
        d = self._generate_data(odoo)
        user = odoo.env['res.users'].browse(d['u0_id'])
        # += List of IDs
        user.groups_id += [d['g1_id'], d['g2_id']]
        data = user.read(['groups_id'])[0]
        self.assertIn(d['g1_id'], data['groups_id'])
        self.assertIn(d['g2_id'], data['groups_id'])
        group_ids = [grp.id for grp in user.groups_id]
        self.assertIn(d['g1_id'], group_ids)
        self.assertIn(d['g2_id'], group_ids)

    @session(login=True)
    def test_field_many2many_write_iadd_list_records(self, odoo):
        d = self._generate_data(odoo)
        user = odoo.env['res.users'].browse(d['u0_id'])
        # += List of records
        user.groups_id += [odoo.env['res.groups'].browse(d['g1_id']),
                           odoo.env['res.groups'].browse(d['g2_id'])]
        data = user.read(['groups_id'])[0]
        self.assertIn(d['g1_id'], data['groups_id'])
        self.assertIn(d['g2_id'], data['groups_id'])
        group_ids = [grp.id for grp in user.groups_id]
        self.assertIn(d['g1_id'], group_ids)
        self.assertIn(d['g2_id'], group_ids)

    @session(login=True)
    def test_field_many2many_write_iadd_id_and_list_ids(self, odoo):
        d = self._generate_data(odoo)
        user = odoo.env['res.users'].browse(d['u0_id'])
        # += ID and += [ID]
        user.groups_id += d['g1_id']
        user.groups_id += [d['g2_id']]
        data = user.read(['groups_id'])[0]
        self.assertIn(d['g1_id'], data['groups_id'])
        self.assertIn(d['g2_id'], data['groups_id'])
        group_ids = [grp.id for grp in user.groups_id]
        self.assertIn(d['g1_id'], group_ids)
        self.assertIn(d['g2_id'], group_ids)

    @session(login=True)
    def test_field_many2many_write_isub_id(self, odoo):
        d = self._generate_data(odoo)
        user = odoo.env['res.users'].browse(d['u1_id'])
        self.assertIn(d['g1_id'], user.groups_id.ids)
        # -= ID
        user.groups_id -= d['g1_id']
        data = user.read(['groups_id'])[0]
        self.assertNotIn(d['g1_id'], data['groups_id'])
        group_ids = [grp.id for grp in user.groups_id]
        self.assertNotIn(d['g1_id'], group_ids)

    @session(login=True)
    def test_field_many2many_write_isub_record(self, odoo):
        d = self._generate_data(odoo)
        user = odoo.env['res.users'].browse(d['u1_id'])
        self.assertIn(d['g1_id'], user.groups_id.ids)
        # -= Record
        group = odoo.env['res.groups'].browse(d['g1_id'])
        user.groups_id -= group
        data = user.read(['groups_id'])[0]
        self.assertNotIn(group.id, data['groups_id'])
        self.assertNotIn(group.id, user.groups_id.ids)

    @session(login=True)
    def test_field_many2many_write_isub_recordset(self, odoo):
        d = self._generate_data(odoo)
        user = odoo.env['res.users'].browse(d['u1_id'])
        groups = odoo.env['res.groups'].browse([d['g1_id'], d['g2_id']])
        # -= Recordset
        data = user.read(['groups_id'])[0]
        self.assertIn(groups.ids[0], data['groups_id'])
        self.assertIn(groups.ids[1], data['groups_id'])
        user.groups_id -= groups
        data = user.read(['groups_id'])[0]
        self.assertNotIn(groups.ids[0], data['groups_id'])
        self.assertNotIn(groups.ids[1], data['groups_id'])
        group_ids = [grp.id for grp in user.groups_id]
        self.assertNotIn(groups.ids[0], group_ids)
        self.assertNotIn(groups.ids[1], group_ids)

    @session(login=True)
    def test_field_many2many_write_isub_list_ids(self, odoo):
        d = self._generate_data(odoo)
        user = odoo.env['res.users'].browse(d['u1_id'])
        groups = odoo.env['res.groups'].browse([d['g1_id'], d['g2_id']])
        # -= List of IDs
        data = user.read(['groups_id'])[0]
        self.assertIn(groups.ids[0], data['groups_id'])
        self.assertIn(groups.ids[1], data['groups_id'])
        user.groups_id -= groups.ids
        data = user.read(['groups_id'])[0]
        self.assertNotIn(groups.ids[0], data['groups_id'])
        self.assertNotIn(groups.ids[1], data['groups_id'])
        group_ids = [grp.id for grp in user.groups_id]
        self.assertNotIn(groups.ids[0], group_ids)
        self.assertNotIn(groups.ids[1], group_ids)

    @session(login=True)
    def test_field_many2many_write_isub_list_records(self, odoo):
        d = self._generate_data(odoo)
        user = odoo.env['res.users'].browse(d['u1_id'])
        groups = odoo.env['res.groups'].browse([d['g1_id'], d['g2_id']])
        # -= List of records
        data = user.read(['groups_id'])[0]
        self.assertIn(groups.ids[0], data['groups_id'])
        self.assertIn(groups.ids[1], data['groups_id'])
        user.groups_id -= [grp for grp in groups]
        data = user.read(['groups_id'])[0]
        self.assertNotIn(groups.ids[0], data['groups_id'])
        self.assertNotIn(groups.ids[1], data['groups_id'])
        group_ids = [grp.id for grp in user.groups_id]
        self.assertNotIn(groups.ids[0], group_ids)
        self.assertNotIn(groups.ids[1], group_ids)

    @session(login=True)
    def test_field_many2many_write_isub_id_and_list_ids(self, odoo):
        d = self._generate_data(odoo)
        user = odoo.env['res.users'].browse(d['u1_id'])
        groups = odoo.env['res.groups'].browse([d['g1_id'], d['g2_id']])
        # -= ID and -= [ID]
        data = user.read(['groups_id'])[0]
        self.assertIn(groups.ids[0], data['groups_id'])
        self.assertIn(groups.ids[1], data['groups_id'])
        user.groups_id -= groups.ids[0]
        user.groups_id -= [groups.ids[1]]
        data = user.read(['groups_id'])[0]
        self.assertNotIn(groups.ids[0], data['groups_id'])
        self.assertNotIn(groups.ids[1], data['groups_id'])
        group_ids = [grp.id for grp in user.groups_id]
        self.assertNotIn(groups.ids[0], group_ids)
        self.assertNotIn(groups.ids[1], group_ids)
