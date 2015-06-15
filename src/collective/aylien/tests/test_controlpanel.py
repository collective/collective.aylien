# -*- coding: utf-8 -*-
from collective.aylien.config import PROJECTNAME
from collective.aylien.interfaces import IPackageSettings
from collective.aylien.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import logout
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']

    def test_controlpanel_has_view(self):
        request = self.layer['request']
        view = api.content.get_view(u'aylien-settings', self.portal, request)
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@aylien-settings')

    def test_controlpanel_installed(self):
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertIn('aylien', actions)

    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']

        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])

        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertNotIn('aylien', actions)


class RegistryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IPackageSettings)

    def test_application_id_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'application_id'))
        self.assertEqual(self.settings.application_id, '')

    def test_application_key_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'application_key'))
        self.assertEqual(self.settings.application_key, '')

    def test_records_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']

        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])

        records = [
            IPackageSettings.__identifier__ + '.application_id',
            IPackageSettings.__identifier__ + '.application_key',
        ]

        for r in records:
            self.assertNotIn(r, self.registry)
