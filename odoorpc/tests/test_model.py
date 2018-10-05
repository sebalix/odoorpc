# -*- coding: utf-8 -*-

from odoorpc.tests import BaseTestCase, session
from odoorpc import error
from odoorpc.models import Model
from odoorpc.env import Environment


class TestModel(BaseTestCase):

    @session(login=True)
    def test_create_model_class(self, odoo):
        partner_model = odoo.env['res.partner']
        self.assertEqual(partner_model._name, 'res.partner')
        self.assertIn('name', partner_model._columns)
        self.assertIsInstance(partner_model.env, Environment)

    @session(login=True)
    def test_model_browse(self, odoo):
        partner_model = odoo.env['res.partner']
        partner = partner_model.browse(1)
        self.assertIsInstance(partner, Model)
        self.assertEqual(partner.id, 1)
        self.assertEqual(partner.ids, [1])
        self.assertEqual(partner.env, partner_model.env)
        partners = partner_model.browse([1])
        self.assertIsInstance(partners, Model)
        self.assertEqual(partners.id, 1)
        self.assertEqual(partners.ids, [1])
        self.assertEqual(partners.env, partner_model.env)
        self.assertEqual(partners.ids, partner.ids)

    @session(login=True)
    def test_model_browse_false(self, odoo):
        partner_model = odoo.env['res.partner']
        partner = partner_model.browse(False)
        self.assertEqual(len(partner), 0)

    @session(login=True)
    def test_model_browse_wrong_id(self, odoo):
        partner_model = odoo.env['res.partner']
        self.assertRaises(
            ValueError,
            partner_model.browse,
            9999999)    # Wrong ID
        self.assertRaises(
            error.RPCError,
            partner_model.browse,
            "1")  # Wrong ID type

    @session(login=True)
    def test_model_browse_without_arg(self, odoo):
        partner_model = odoo.env['res.partner']
        self.assertRaises(TypeError, partner_model.browse)

    @session(login=True)
    def test_model_rpc_method(self, odoo):
        user_obj = odoo.env['res.users']
        user_obj.name_get(odoo.env.uid)
        odoo.env['ir.sequence'].get('fake.code')  # Return False

    @session(login=True)
    def test_model_rpc_method_error_no_arg(self, odoo):
        # Handle exception (execute a 'name_get' with without args)
        user_obj = odoo.env['res.users']
        self.assertRaises(
            error.RPCError,
            user_obj.name_get)  # No arg

    @session(login=True)
    def test_model_rpc_method_error_wrong_args(self, odoo):
        # Handle exception (execute a 'search' with wrong args)
        user_obj = odoo.env['res.users']
        self.assertRaises(
            error.RPCError,
            user_obj.search,
            False)  # Wrong arg

    @session(login=True)
    def test_record_getitem_field(self, odoo):
        partner_model = odoo.env['res.partner']
        partner = partner_model.browse(1)
        self.assertEqual(partner['id'], 1)
        self.assertEqual(partner['name'], partner.name)

    @session(login=True)
    def test_record_getitem_integer(self, odoo):
        partner_model = odoo.env['res.partner']
        partner = partner_model.browse(1)
        self.assertEqual(partner[0], partner)

    @session(login=True)
    def test_record_getitem_slice(self, odoo):
        partner_model = odoo.env['res.partner']
        partner = partner_model.browse(1)
        self.assertEqual([record.id for record in partner[:]], [1])

    @session(login=True)
    def test_record_iter(self, odoo):
        partner_model = odoo.env['res.partner']
        ids = partner_model.search([])[:5]
        partners = partner_model.browse(ids)
        self.assertEqual(set([partner.id for partner in partners]), set(ids))
        partner = partners[0]
        self.assertIn(partner.id, partners.ids)
        self.assertEqual(id(partner._values), id(partners._values))

    @session(login=True)
    def test_record_with_context(self, odoo):
        user = odoo.env.user
        self.assertEqual(user.env.lang, 'en_US')
        user_fr = user.with_context(lang='fr_FR')
        self.assertEqual(user_fr.env.lang, 'fr_FR')
        # Install 'fr_FR' and test the use of context with it
        Wizard = odoo.env['base.language.install']
        wiz_id = Wizard.create({'lang': 'fr_FR'})
        Wizard.lang_install([wiz_id])
        # Read data with two languages
        Country = odoo.env['res.country']
        de_id = Country.search([('code', '=', 'DE')])[0]
        de = Country.browse(de_id)
        self.assertEqual(de.name, 'Germany')
        self.assertEqual(de.with_context(lang='fr_FR').name, 'Allemagne')
        # Write data with two languages
        Product = odoo.env['product.product']
        self.assertEqual(Product.env.lang, 'en_US')
        name_en = "Product en_US"
        product_id = Product.create({'name': name_en})
        product_en = Product.browse(product_id)
        self.assertEqual(product_en.name, name_en)
        product_fr = product_en.with_context(lang='fr_FR')
        self.assertEqual(product_fr.env.lang, 'fr_FR')
        name_fr = "Produit fr_FR"
        product_fr.write({'name': name_fr})
        product_fr = product_fr.with_context()  # Refresh the recordset
        self.assertEqual(product_fr.name, name_fr)
        self.assertEqual(Product.env.lang, 'en_US')
        product_en = Product.browse(product_id)
        self.assertEqual(product_en.name, name_en)
        new_name_fr = "%s (nouveau)" % name_fr
        product_fr.name = new_name_fr
        product_fr = product_fr.with_context()  # Refresh the recordset
        self.assertEqual(product_fr.name, new_name_fr)
