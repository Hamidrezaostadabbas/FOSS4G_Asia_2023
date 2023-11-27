"""
common functions of PYQGIS
"""

from qgis.core import QgsVectorLayer, QgsProject
from qgis.utils import iface

import os


def get_script_path_plugin():
    return os.path.dirname(__file__)


def import_vector_layer(layer_path, layer_name):
    layer = QgsVectorLayer(layer_path, layer_name)
    return layer if layer.isValid() else None


def display_vector_layer(layer, name=None):
    displayed_layer = QgsProject.instance().addMapLayer(layer)
    if name:
        displayed_layer.setName(name)


def zoom_to_layer(layer):
    canvas = iface.mapCanvas()
    extent = layer.extent()
    canvas.setExtent(extent)
    canvas.refresh()


def qml_loader(layer, layer_symbol_path):
    layer.loadNamedStyle(layer_symbol_path)
    layer.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(layer.id())
    QgsProject.instance().addMapLayers([layer], False)
