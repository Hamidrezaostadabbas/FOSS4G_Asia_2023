"""
layout settings
"""
from qgis.core import QgsProject, QgsPrintLayout, QgsLayoutPoint, QgsUnitTypes, QgsLayoutItemLabel, QgsLayerTree, \
    QgsLayoutItemPicture, QgsLayoutItemScaleBar, QgsLayoutItemLegend, QgsLegendStyle, QgsLayoutSize, \
    QgsLayoutItemPage, QgsLayoutItemMap, QgsLayoutMeasurement, QgsLayoutExporter, QgsTextBackgroundSettings

from PyQt5.QtGui import QColor, QFont


def __layout_creator(plan_name):
    project = QgsProject.instance()
    layout_manager = QgsProject.instance().layoutManager()
    layout_lists = layout_manager.printLayouts()
    for layout in layout_lists:
        if layout.name() == plan_name:
            layout_manager.removeLayout(layout)
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.setName(plan_name)
    layout_manager.addLayout(layout)
    layout.pageCollection().page(0).setPageSize('A3', QgsLayoutItemPage.Orientation.Landscape)
    return layout


def __layout_map_window_creator(layer, layout, start_x, start_y, width, height):
    map_window = QgsLayoutItemMap(layout)
    map_window.setRect(1, 1, 1, 1)
    map_window.attemptMove(QgsLayoutPoint(start_x, start_y, QgsUnitTypes.LayoutMillimeters))
    map_window.attemptResize(QgsLayoutSize(width, height, QgsUnitTypes.LayoutMillimeters))
    map_window.zoomToExtent(layer.extent())
    map_window.keepLayerStyles()
    map_window.setFrameStrokeWidth(QgsLayoutMeasurement(0.1))
    map_window.setFrameEnabled(True)
    layout.addLayoutItem(map_window)


def __layout_label_creator(
        layout, start_x, start_y, width, height, text='', text_color=QColor(), font_size=10,
        font_weight='regular', font_type='Arial', background_color=None
):
    label = QgsLayoutItemLabel(layout)
    label.setText(text)
    if font_weight == 'regular':
        label.setFont(QFont(f"{font_type}", font_size))
    else:
        label.setFont(QFont(f"{font_type}", font_size, QFont.Bold))
    label.setFontColor(text_color)
    if background_color is not None:
        label.setBackgroundColor(background_color)
        label.setBackgroundEnabled(True)

    label.adjustSizeToText()
    label.attemptMove(QgsLayoutPoint(start_x, start_y, QgsUnitTypes.LayoutMillimeters))
    label.attemptResize(QgsLayoutSize(width, height))
    layout.addLayoutItem(label)


def __layout_legend_creator(layout, legend_layers, start_x, start_y, width, height):
    legend = QgsLayoutItemLegend(layout)
    legend.setAutoUpdateModel(False)
    group = legend.model().rootGroup()
    group.clear()
    for layer in legend_layers:
        group.addLayer(layer)
    legend.setStyleFont(QgsLegendStyle.Subgroup, QFont('Arial', 10, QFont.Bold))
    legend.setStyleFont(QgsLegendStyle.SymbolLabel, QFont('Arial', 8))
    legend.setSymbolHeight(5.5)
    legend.setSymbolWidth(9.5)
    legend.rstyle(QgsLegendStyle.Title).setMargin(QgsLegendStyle.Bottom, 0)
    legend.rstyle(QgsLegendStyle.Group).setMargin(QgsLegendStyle.Top, 4)
    legend.rstyle(QgsLegendStyle.Subgroup).setMargin(QgsLegendStyle.Top, 4)
    legend.rstyle(QgsLegendStyle.SymbolLabel).setMargin(QgsLegendStyle.Left, 4)
    legend.rstyle(QgsLegendStyle.Symbol).setMargin(QgsLegendStyle.Top, 3)
    legend.attemptResize(QgsLayoutSize(width, height))
    legend.attemptMove(QgsLayoutPoint(start_x, start_y, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(legend)


def __layout_pdf_exporter(layout, pdf_path):
    exporter = QgsLayoutExporter(layout)
    exporter.exportToPdf(pdf_path, QgsLayoutExporter.PdfExportSettings())


def layout_executor(
        layers_name, layout_title, city_name, pdf_path
):
    legend_layers = []
    for layer_name in layers_name:
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        legend_layers.append(layer)
    layout = __layout_creator(layout_title)
    __layout_map_window_creator(layer, layout, 20, 7, 294, 285)
    __layout_label_creator(layout, 23, 266, 82, 24, background_color=QColor(255, 255, 255))
    __layout_label_creator(
        layout, 320, 5, 96, 6, layout_title, QColor(0, 182, 228),
        14, 'bold', 'Arial'
    )
    __layout_legend_creator(layout, legend_layers, 319, 12, 98, 186)
    __layout_label_creator(
        layout, 320, 220, 96, 20, 'City Name', QColor(0, 182, 228), 20,
        'bold', 'Arial'
    )
    __layout_label_creator(layout, 320, 230, 96, 20, city_name, QColor(), 16)
    __layout_pdf_exporter(layout, pdf_path)
