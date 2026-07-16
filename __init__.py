# -*- coding: utf-8 -*-
"""
This script initializes the PeruSpatial Hub plugin.
"""

def classFactory(iface):
    """Load PeruSpatialHub class from peruspatial_hub.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    from .peruspatial_hub import PeruSpatialHub
    return PeruSpatialHub(iface)
