# -*- coding: utf-8 -*-
from collective.aylien import _
from plone.directives import form
from zope import schema
from zope.interface import Interface


class IBrowserLayer(Interface):

    """A layer specific for this add-on product."""


class IPackageSettings(form.Schema):

    """Schema for the control panel form."""

    application_id = schema.ASCIILine(
        title=_(u'Application ID'),
        description=_(u''),
        required=True,
        default='',
    )

    application_key = schema.ASCIILine(
        title=_(u'Application Key'),
        description=_(u''),
        required=True,
        default='',
    )
