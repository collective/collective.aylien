# -*- coding: utf-8 -*-
from collective.aylien import _
from collective.aylien.interfaces import IPackageSettings
from plone.app.registry.browser import controlpanel


class PackageSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IPackageSettings
    label = _(u'Package Settings')
    description = _(u'Here you can modify the settings for collective.aylien.')


class PackageSettingsControlPanel(controlpanel.ControlPanelFormWrapper):

    form = PackageSettingsEditForm
