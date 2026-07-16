# -*- coding: utf-8 -*-
"""
Dockable panel UI for PeruSpatial Hub.
Constructed programmatically via PyQt5.
"""

import os
import webbrowser
import urllib.parse
import http.client
import json
import ssl
import time
import unicodedata

from qgis.PyQt.QtCore import Qt, QSize, QTimer
from qgis.PyQt.QtWidgets import (
    QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLineEdit, QComboBox, QTreeWidget, QTreeWidgetItem, QPushButton, QToolButton,
    QLabel, QTextBrowser, QMessageBox, QSplitter, QDialog, QDialogButtonBox
)
from qgis.PyQt.QtGui import QFont, QColor, QClipboard, QIcon, QPixmap
from qgis.core import QgsSettings, QgsRasterLayer, QgsVectorLayer, QgsProject, QgsDataSourceUri, QgsCoordinateReferenceSystem

ARCGIS_SERVICE_TYPES = {
    "arcgis_mapserver": "MapServer",
    "arcgisfeatureserver": "FeatureServer",
    "arcgis_imageserver": "ImageServer",
}

ACTIVE_REST_ROOTS = {
    "https://geocatmin.ingemmet.gob.pe/arcgis/rest/services",
    "https://geocatmin.ingemmet.gob.pe/arcgis/rest/services/WGS84_18",
    "https://www.idep.gob.pe/geoportal/rest/services/SERVICIOS_IGN",
    "https://www.idep.gob.pe/geoportal/rest/services/INSTITUCIONALES",
    "https://geoservicios.sernanp.gob.pe/arcgis/rest/services",
    "https://geoservidorperu.minam.gob.pe/arcgis/rest/services",
    "https://geo.serfor.gob.pe/geoservicios/rest/services",
    "https://sigda.cultura.gob.pe/sigda/rest/services",
    "https://gisem.osinergmin.gob.pe/serverosih/rest/services",
    "https://pifa.oefa.gob.pe/arcgis/rest/services",
}

ACTIVE_WMS_ROOTS = {
    "https://ide.igp.gob.pe/geoserver/ows",
}

CATALOG_CATEGORIES = [
    "Arqueología y Cultura",
    "Clima y Riesgos",
    "Geología y Minería",
    "Hidrología y Agua",
    "Límites y Cartografía",
    "Medio Ambiente",
]

MAX_HTTP_RESPONSE_BYTES = 20 * 1024 * 1024


def _read_https(url, timeout=15, headers=None):
    """Read a bounded HTTPS response using certificate verification."""
    parts = urllib.parse.urlsplit(url)
    if parts.scheme.casefold() != "https" or not parts.hostname:
        raise ValueError("solo se permiten servicios HTTPS con un host válido")

    path = parts.path or "/"
    if parts.query:
        path = f"{path}?{parts.query}"

    connection = http.client.HTTPSConnection(
        parts.hostname,
        port=parts.port or 443,
        timeout=timeout,
        context=ssl.create_default_context(),
    )
    try:
        connection.request("GET", path, headers=headers or {})
        response = connection.getresponse()
        if response.status < 200 or response.status >= 300:
            raise RuntimeError(f"HTTP {response.status}: {response.reason}")
        payload = response.read(MAX_HTTP_RESPONSE_BYTES + 1)
        if len(payload) > MAX_HTTP_RESPONSE_BYTES:
            raise RuntimeError("la respuesta del servidor excede el límite permitido")
        return payload
    finally:
        connection.close()


def _url_with_json(url):
    """Return an ArcGIS REST URL with f=json without damaging existing queries."""
    parts = urllib.parse.urlsplit(url)
    query = dict(urllib.parse.parse_qsl(parts.query, keep_blank_values=True))
    query["f"] = "json"
    return urllib.parse.urlunsplit(
        (parts.scheme, parts.netloc, parts.path, urllib.parse.urlencode(query), parts.fragment)
    )


def _clean_rest_url(url):
    parts = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc, parts.path.rstrip("/"), "", ""))


def _append_rest_path(url, *segments):
    base = _clean_rest_url(url)
    encoded = [urllib.parse.quote(str(segment).strip("/"), safe="") for segment in segments]
    return "/".join([base] + encoded)


def _service_url(directory_url, service_name, service_type):
    """Build the service URL returned by an ArcGIS REST directory."""
    base = _clean_rest_url(directory_url)
    name_parts = [part for part in str(service_name).split("/") if part]
    current_folder = urllib.parse.unquote(urllib.parse.urlsplit(base).path.rstrip("/").split("/")[-1])
    if len(name_parts) > 1 and name_parts[0].lower() == current_folder.lower():
        name_parts = name_parts[1:]
    return _append_rest_path(base, *name_parts, service_type)

class AboutDialog(QDialog):
    def __init__(self, parent=None, plugin_dir=None):
        super().__init__(parent)
        self.setWindowTitle("Acerca de PeruSpatial Hub")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 20)
        layout.setSpacing(15)

        logo_label = QLabel()
        logo_path = os.path.join(plugin_dir, "logo_dev.png") if plugin_dir else ""
        pixmap = QPixmap(logo_path)
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap.scaledToHeight(80, Qt.TransformationMode.SmoothTransformation))
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(logo_label)

        title = QLabel("<h2>PeruSpatial Hub</h2>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel(
            "Desarrollado por <b>Jordan Zavaleta (GisGeo Dev)</b><br>"
            "<a href='mailto:jordanzav@gisgeo.dev' style='text-decoration: none; color: #1976d2;'>jordanzav@gisgeo.dev</a>"
        )
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setOpenExternalLinks(True)
        layout.addWidget(subtitle)

        links = QLabel(
            "<a href='https://gisgeo.dev' style='text-decoration: none; color: #1976d2;'>Sitio Web: gisgeo.dev</a><br><br>"
            "<a href='https://www.linkedin.com/in/jordan-zav/' style='text-decoration: none; color: #1976d2;'>LinkedIn Profile</a>"
        )
        links.setAlignment(Qt.AlignmentFlag.AlignCenter)
        links.setOpenExternalLinks(True)
        layout.addWidget(links)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

        self.setStyleSheet(
            "QDialog { background-color: white; } QLabel { color: #333; }"
        )


class ServiceStatusDialog(QDialog):
    """Explains why researched institutions may not appear in the catalog."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Estado de servicios investigados")
        self.setMinimumSize(560, 430)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 12)
        layout.setSpacing(10)

        title = QLabel("<h2>Servicios investigados</h2>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        details = QTextBrowser()
        details.setOpenExternalLinks(True)
        details.setHtml(
            "<p>PeruSpatial Hub revisó estas instituciones. Si alguna no aparece como "
            "conexión disponible, no significa que haya sido omitida sin investigación.</p>"
            "<ul>"
            "<li><b>OEFA:</b> el directorio público PIFA está operativo y ya se encuentra "
            "integrado en el catálogo.</li>"
            "<li><b>SUNARP:</b> el Visor BGR solicita DNI, fecha de emisión y captcha. "
            "No se encontró un directorio REST anónimo verificado para integrarlo como "
            "las demás conexiones.</li>"
            "<li><b>CENEPRED:</b> SIGRID dispone de acceso de usuario, pero actualmente "
            "el ArcGIS Web Adaptor público informa que no puede comunicarse con su "
            "servidor interno. Iniciar sesión no corrige esa falla del servicio REST.</li>"
            "<li><b>COFOPRI:</b> el servidor conocido presenta problemas de validación "
            "del certificado TLS y la ruta REST consultada responde HTTP 404. Por "
            "seguridad, el plugin no desactiva la validación de certificados.</li>"
            "</ul>"
            "<p><b>Trabajo futuro:</b> se continuarán explorando nuevas URL oficiales y "
            "la posible integración de servicios con inicio de sesión, siempre que exista "
            "un mecanismo autorizado y seguro. Las credenciales no se incluirán ni se "
            "guardarán directamente en el plugin.</p>"
            "<p><i>Estado revisado para la versión 1.0.0.</i></p>"
        )
        layout.addWidget(details)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)


class PeruSpatialHubPanel(QDockWidget):
    def __init__(self, iface, parent=None, plugin_dir=None):
        super(PeruSpatialHubPanel, self).__init__(parent)
        self.iface = iface
        self.plugin_dir = plugin_dir
        self.setWindowTitle("PeruSpatial Hub")
        self.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea
            | Qt.DockWidgetArea.RightDockWidgetArea
        )

        # Set main widget
        self.main_widget = QWidget()
        self.setWidget(self.main_widget)
        
        # Main layout
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(8, 8, 8, 8)
        self.main_layout.setSpacing(8)

        # 1. Header Widget (Logo and Title)
        self.init_header()

        # Create a splitter to separate the search/tree section from the metadata/actions section
        self.splitter = QSplitter(Qt.Orientation.Vertical)
        self.main_layout.addWidget(self.splitter)

        # Top container for search and list
        self.top_container = QWidget()
        self.top_layout = QVBoxLayout(self.top_container)
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.setSpacing(6)

        # 2. Search & Filter Bar
        self.init_search_filters()

        # 3. Main Tree Widget (Catalog)
        self.init_tree_widget()
        
        self.top_layout.addWidget(self.search_filter_widget)
        self.top_layout.addWidget(self.tree_widget)
        self.splitter.addWidget(self.top_container)

        # Bottom container for metadata and actions
        self.bottom_container = QWidget()
        self.bottom_layout = QVBoxLayout(self.bottom_container)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout.setSpacing(6)

        # 4. Metadata details (QTextBrowser)
        self.init_metadata_panel()

        # 5. Action Buttons (Grid Layout)
        self.init_action_buttons()

        # 6. CRS Warning Banner
        self.init_crs_warning_banner()

        self.bottom_layout.addWidget(self.metadata_panel)
        self.bottom_layout.addWidget(self.crs_banner)
        self.bottom_layout.addWidget(self.button_grid_widget)
        self.splitter.addWidget(self.bottom_container)

        # Set default splitter sizes (give tree more space than metadata)
        self.splitter.setSizes([350, 250])

        # Load services into Tree
        self.populate_tree()

        # Directory discovery is deferred until the user searches, avoiding
        # unnecessary network traffic when the catalog is only browsed manually.
        self._directory_catalog_loaded = False
        self._discovering_catalog = False
        self.search_timer = QTimer(self)
        self.search_timer.setSingleShot(True)
        self.search_timer.setInterval(500)
        self.search_timer.timeout.connect(self.perform_deep_search)
        
        # Connect signals
        self.search_input.textChanged.connect(self.schedule_filter_services)
        self.category_combo.currentIndexChanged.connect(self.filter_services)
        self.tree_widget.itemSelectionChanged.connect(self.on_selection_changed)
        self.tree_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.tree_widget.itemExpanded.connect(self.on_item_expanded)

        # Initial state
        self.update_buttons_state(None)

    def init_header(self):
        """Creates the header title, logo and description."""
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(2, 2, 2, 2)
        header_layout.setSpacing(4)

        # Logo Centered (GisGeo)
        logo_label = QLabel()
        logo_path = os.path.join(self.plugin_dir, "logo.png") if self.plugin_dir else ""
        pixmap = QPixmap(logo_path)
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap.scaledToHeight(60, Qt.TransformationMode.SmoothTransformation))
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            header_layout.addWidget(logo_label)

        title_label = QLabel("PeruSpatial Hub")
        title_font = QFont("Segoe UI", 12, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #0b5394;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sub_label = QLabel("Catálogo de Geoportales y Servidores del Estado Peruano")
        sub_font = QFont("Segoe UI", 8, QFont.Style.StyleItalic)
        sub_label.setFont(sub_font)
        sub_label.setStyleSheet("color: #555;")
        sub_label.setWordWrap(True)
        sub_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_layout.addWidget(title_label)
        header_layout.addWidget(sub_label)
        self.main_layout.addWidget(header_widget)

    def init_search_filters(self):
        """Creates search box and category filter combo."""
        self.search_filter_widget = QWidget()
        layout = QHBoxLayout(self.search_filter_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar servicio o capa (ej. sismos, catastro)...")
        self.search_input.setClearButtonEnabled(True)

        self.category_combo = QComboBox()
        self.category_combo.addItem("Todas las Categorías")
        self.category_combo.addItems(CATALOG_CATEGORIES)
        self.category_combo.setFixedWidth(130)

        self.btn_service_status = QToolButton()
        self.btn_service_status.setText("ⓘ")
        self.btn_service_status.setToolTip(
            "Ver el estado de instituciones y servicios investigados"
        )
        self.btn_service_status.setAccessibleName("Información de servicios investigados")
        self.btn_service_status.setFixedSize(30, 30)
        self.btn_service_status.clicked.connect(self.show_service_status_dialog)

        layout.addWidget(self.search_input)
        layout.addWidget(self.category_combo)
        layout.addWidget(self.btn_service_status)

    def init_tree_widget(self):
        """Creates tree widget for service categories and list."""
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Servicio / Institución", "Tipo"])
        self.tree_widget.setHeaderHidden(False)
        self.tree_widget.setColumnWidth(0, 220)
        self.tree_widget.setColumnWidth(1, 100)
        self.tree_widget.setAlternatingRowColors(True)
        self.tree_widget.setStyleSheet("""
            QTreeWidget {
                border: 1px solid #dcdcdc;
                background-color: #ffffff;
            }
            QTreeWidget::item {
                padding: 4px;
            }
        """)

    def init_metadata_panel(self):
        """Creates the text panel to show metadata details."""
        self.metadata_panel = QTextBrowser()
        self.metadata_panel.setOpenExternalLinks(True)
        self.metadata_panel.setPlaceholderText("Seleccione un servicio para ver los detalles, URLs y metadatos.")
        self.metadata_panel.setStyleSheet("""
            QTextBrowser {
                border: 1px solid #dcdcdc;
                background-color: #f9f9f9;
                font-family: 'Segoe UI', Arial;
                font-size: 11px;
            }
        """)

    def init_crs_warning_banner(self):
        """Creates a dedicated banner warning about CRS and Datum accuracy."""
        self.crs_banner = QLabel()
        self.crs_banner.setWordWrap(True)
        self.crs_banner.setStyleSheet("""
            QLabel {
                background-color: #fff2cc;
                border: 1px solid #ffe599;
                color: #7f6000;
                padding: 6px;
                border-radius: 4px;
                font-family: 'Segoe UI';
                font-size: 10.5px;
            }
        """)
        # Default text explaining general rules for Peru spatial
        self.crs_banner.setText(
            "<b>💡 Nota de Precisión (Geofísica/Arqueología):</b><br>"
            "Los levantamientos de precisión requieren el datum correcto. Asegúrese de "
            "configurar su proyecto QGIS en el huso UTM adecuado (ej. <b>WGS84 / UTM 18S</b> - EPSG:32718). "
            "Si usa capas históricas en <b>PSAD56</b>, aplique la transformación a WGS84 para evitar desfases."
        )

    def init_action_buttons(self):
        """Creates action buttons grouped at the bottom."""
        self.button_grid_widget = QWidget()
        grid = QGridLayout(self.button_grid_widget)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(4)

        self.btn_add_layer = QPushButton("Añadir al Mapa")
        self.btn_add_layer.setStyleSheet("background-color: #4caf50; color: white; font-weight: bold; padding: 6px;")
        
        self.btn_register_browser = QPushButton("Registrar Conexión")
        self.btn_register_browser.setStyleSheet("padding: 6px;")

        self.btn_register_all = QPushButton("Registrar Todo")
        self.btn_register_all.setStyleSheet("background-color: #0b5394; color: white; padding: 6px;")
        
        self.btn_copy_url = QPushButton("Copiar URL")
        self.btn_copy_url.setStyleSheet("padding: 6px;")

        self.btn_open_browser = QPushButton("Ver en Web")
        self.btn_open_browser.setStyleSheet("padding: 6px;")

        self.btn_about = QPushButton("Acerca de")
        self.btn_about.setStyleSheet("padding: 6px;")

        # Grid configuration
        grid.addWidget(self.btn_add_layer, 0, 0)
        grid.addWidget(self.btn_register_browser, 0, 1)
        grid.addWidget(self.btn_copy_url, 1, 0)
        grid.addWidget(self.btn_open_browser, 1, 1)
        grid.addWidget(self.btn_register_all, 2, 0)
        grid.addWidget(self.btn_about, 2, 1)

        # Event handlers
        self.btn_add_layer.clicked.connect(self.add_selected_layer)
        self.btn_register_browser.clicked.connect(self.register_selected_connection)
        self.btn_register_all.clicked.connect(self.register_all_connections)
        self.btn_copy_url.clicked.connect(self.copy_selected_url)
        self.btn_open_browser.clicked.connect(self.open_selected_web)
        self.btn_about.clicked.connect(self.show_about_dialog)

    def show_about_dialog(self):
        """Opens the About dialog with developer information and links."""
        dialog = AboutDialog(self, self.plugin_dir)
        dialog.exec()

    def show_service_status_dialog(self):
        """Shows the research status of unavailable or restricted services."""
        dialog = ServiceStatusDialog(self)
        dialog.exec()

    def fetch_arcgis_json(self, url, timeout=15, attempts=2):
        """Read ArcGIS REST metadata with one retry for intermittent public servers."""
        request_url = _url_with_json(url)
        last_error = None
        for attempt in range(attempts):
            try:
                payload = _read_https(
                    request_url,
                    timeout=timeout,
                    headers={
                        "User-Agent": "PeruSpatial-Hub-QGIS/1.0.0",
                        "Accept": "application/json",
                    },
                )
                data = json.loads(payload.decode("utf-8-sig"))
                if not isinstance(data, dict):
                    raise ValueError("el servidor no devolvió un objeto JSON")
                if data.get("error"):
                    error = data["error"]
                    details = "; ".join(error.get("details") or [])
                    message = error.get("message") or "error REST sin descripción"
                    raise RuntimeError(f"ArcGIS REST {error.get('code', '')}: {message}. {details}".strip())
                return data
            except (
                OSError,
                http.client.HTTPException,
                ValueError,
                RuntimeError,
                json.JSONDecodeError,
            ) as exc:
                last_error = exc
                if attempt + 1 < attempts:
                    time.sleep(0.35)
        raise RuntimeError(f"No se pudo consultar {request_url}: {last_error}")

    @staticmethod
    def service_kind_from_url(url, stype=None):
        if stype in ARCGIS_SERVICE_TYPES:
            return ARCGIS_SERVICE_TYPES[stype]
        path = urllib.parse.urlsplit(url).path.rstrip("/")
        ending = path.split("/")[-1]
        if ending in ("MapServer", "FeatureServer", "ImageServer"):
            return ending
        return None


    def populate_tree(self):
        """Fills the TreeWidget grouping services by institution and adding live servers."""
        self.tree_widget.clear()
        
        # The old fixed layer URLs contained many retired services. Start from
        # live repository roots and discover their current services/layers.
        explorer_root = QTreeWidgetItem(self.tree_widget)
        explorer_root.setText(0, "🌐 Servidores en Vivo (Explorador Completo)")
        explorer_root.setFont(0, QFont("Segoe UI", 10, QFont.Weight.Bold))
        explorer_root.setForeground(0, QColor("#0b5394"))
        explorer_root.setData(0, Qt.ItemDataRole.UserRole, None)

        # List of official directories/servers for live exploration
        LIVE_SERVERS = [
            {
                "institution": "INGEMMET (GEOCATMIN)",
                "name": "Servicios REST Generales (WGS84)",
                "url": "https://geocatmin.ingemmet.gob.pe/arcgis/rest/services",
                "stype": "arcgis_rest",
                "category": "Geología y Minería"
            },
            {
                "institution": "INGEMMET (GEOCATMIN)",
                "name": "Servicios REST Huso 18S (WGS84)",
                "url": "https://geocatmin.ingemmet.gob.pe/arcgis/rest/services/WGS84_18",
                "stype": "arcgis_rest",
                "category": "Geología y Minería"
            },
            {
                "institution": "IGN",
                "name": "IGN Servicios de Cartografía (REST)",
                "url": "https://www.idep.gob.pe/geoportal/rest/services/SERVICIOS_IGN",
                "stype": "arcgis_rest",
                "category": "Límites y Cartografía"
            },
            {
                "institution": "IDEP (ANA y otras instituciones)",
                "name": "Servicios Institucionales Oficiales (REST)",
                "url": "https://www.idep.gob.pe/geoportal/rest/services/INSTITUCIONALES",
                "stype": "arcgis_rest",
                "category": "Hidrología y Agua"
            },
            {
                "institution": "MINCUL",
                "name": "MINCUL Patrimonio y Arqueología (REST)",
                "url": "https://sigda.cultura.gob.pe/sigda/rest/services",
                "stype": "arcgis_rest",
                "category": "Arqueología y Cultura",
                "crs_warning": True
            },
            {
                "institution": "SERNANP",
                "name": "SERNANP Áreas Protegidas (REST)",
                "url": "https://geoservicios.sernanp.gob.pe/arcgis/rest/services",
                "stype": "arcgis_rest",
                "category": "Medio Ambiente"
            },
            {
                "institution": "SERFOR",
                "name": "SERFOR Catastro Forestal (REST)",
                "url": "https://geo.serfor.gob.pe/geoservicios/rest/services",
                "stype": "arcgis_rest",
                "category": "Medio Ambiente"
            },
            {
                "institution": "MINAM",
                "name": "MINAM Geoservidor (REST)",
                "url": "https://geoservidorperu.minam.gob.pe/arcgis/rest/services",
                "stype": "arcgis_rest",
                "category": "Medio Ambiente"
            },
            {
                "institution": "OSINERGMIN",
                "name": "OSINERGMIN Energía (REST)",
                "url": "https://gisem.osinergmin.gob.pe/serverosih/rest/services",
                "stype": "arcgis_rest",
                "category": "Límites y Cartografía"
            },
            {
                "institution": "OEFA",
                "name": "PIFA Monitoreo y Fiscalización Ambiental (REST)",
                "url": "https://pifa.oefa.gob.pe/arcgis/rest/services",
                "stype": "arcgis_rest",
                "category": "Medio Ambiente"
            },
            {
                "institution": "IGP",
                "name": "IGP Sismos y Vulcanología (WMS)",
                "url": "https://ide.igp.gob.pe/geoserver/ows?service=wms",
                "stype": "wms",
                "category": "Clima y Riesgos"
            },
        ]

        self.live_servers = [
            s for s in LIVE_SERVERS
            if (
                s["stype"] == "arcgis_rest"
                and _clean_rest_url(s["url"]) in ACTIVE_REST_ROOTS
            ) or (
                s["stype"] == "wms"
                and _clean_rest_url(s["url"]) in ACTIVE_WMS_ROOTS
            )
        ]
        for s in self.live_servers:
            server_item = QTreeWidgetItem(explorer_root)
            server_item.setText(0, f"{s['institution']} - {s['name']}")
            is_arcgis = s["stype"] == "arcgis_rest"
            server_item.setText(1, "Servidor ArcGIS REST" if is_arcgis else "Servidor WMS")
            server_item.setData(0, Qt.ItemDataRole.UserRole, {
                "type": "server" if is_arcgis else "ogc_service",
                "stype": s["stype"],
                "url": s["url"],
                "name": s["name"],
                "institution": s["institution"],
                "category": s["category"],
                "crs_warning": s.get("crs_warning", False),
                "is_loaded": not is_arcgis
            })
            if is_arcgis:
                # Add a dummy child to show expansion arrow
                dummy = QTreeWidgetItem(server_item)
                dummy.setText(0, "Cargando...")

        # Keep root items expanded, but explorer root collapsed by default
        self.tree_widget.expandAll()
        explorer_root.setExpanded(False)

    def friendly_type(self, type_str):
        """Translates technical connection type to friendly name."""
        mapping = {
            "arcgis_mapserver": "Raster/Vectorial REST",
            "arcgisfeatureserver": "Vectorial REST",
            "arcgis_imageserver": "Raster REST",
            "arcgis_map_layer": "Capa REST",
            "arcgis_vector_layer": "Vectorial REST",
            "arcgis_raster_layer": "Raster REST",
            "wms": "Servidor WMS",
        }
        return mapping.get(type_str, type_str)

    @staticmethod
    def normalize_search_text(value):
        """Normalize case and accents so geologia also matches Geología."""
        normalized = unicodedata.normalize("NFKD", str(value or ""))
        return "".join(char for char in normalized if not unicodedata.combining(char)).casefold()

    def item_matches_search(self, item, search_text, selected_category):
        """Return whether one tree node matches the active text/category filters."""
        data = item.data(0, Qt.ItemDataRole.UserRole) or {}
        category = data.get("category")
        category_matches = (
            selected_category == "Todas las Categorías"
            or category is None
            or category == selected_category
        )
        if not category_matches:
            return False
        if not search_text:
            return True

        searchable_values = [
            item.text(0),
            item.text(1),
            data.get("name", ""),
            data.get("institution", ""),
            data.get("description", ""),
            data.get("url", ""),
        ]
        searchable_values.extend(data.get("tags", []))
        return any(
            search_text in self.normalize_search_text(value)
            for value in searchable_values
        )

    @staticmethod
    def set_descendants_hidden(item, hidden):
        """Apply visibility to all descendants of a matching container."""
        for index in range(item.childCount()):
            child = item.child(index)
            child.setHidden(hidden)
            PeruSpatialHubPanel.set_descendants_hidden(child, hidden)

    def filter_tree_item(self, item, search_text, selected_category):
        """Filter a complete branch and retain ancestors of matching layers."""
        own_match = self.item_matches_search(item, search_text, selected_category)
        descendant_match = False

        for index in range(item.childCount()):
            child = item.child(index)
            if self.filter_tree_item(child, search_text, selected_category):
                descendant_match = True

        visible = own_match or descendant_match
        item.setHidden(not visible)

        # When a folder/service itself matches, show its complete loaded subtree.
        # This makes searches such as 100k reveal the layers contained by it.
        if own_match and search_text:
            self.set_descendants_hidden(item, False)

        if search_text and descendant_match:
            item.setExpanded(True)
        return visible

    def filter_services(self):
        """Filter every tree level, including folders, groups and REST layers."""
        search_text = self.normalize_search_text(self.search_input.text().strip())
        selected_category = self.category_combo.currentText()

        for i in range(self.tree_widget.topLevelItemCount()):
            self.filter_tree_item(
                self.tree_widget.topLevelItem(i), search_text, selected_category
            )

    def schedule_filter_services(self):
        """Filter loaded nodes now and defer remote directory discovery."""
        self.filter_services()
        if self.search_input.text().strip():
            self.search_timer.start()
        else:
            self.search_timer.stop()

    def iter_tree_items(self, parent=None):
        """Yield all items below a parent, or the complete tree when omitted."""
        if parent is None:
            items = [
                self.tree_widget.topLevelItem(index)
                for index in range(self.tree_widget.topLevelItemCount())
            ]
        else:
            items = [parent.child(index) for index in range(parent.childCount())]

        for item in items:
            yield item
            yield from self.iter_tree_items(item)

    def discover_directory_branch(self, item, visited):
        """Load REST folders/services recursively, without loading every service layer."""
        data = item.data(0, Qt.ItemDataRole.UserRole) or {}
        if data.get("type") not in ("server", "folder"):
            return

        url = _clean_rest_url(data.get("url", ""))
        if not url or url in visited:
            return
        visited.add(url)

        if not data.get("is_loaded", False):
            self.load_dynamic_node(item)

        # Snapshot children because loading a branch replaces its dummy node.
        children = [item.child(index) for index in range(item.childCount())]
        for child in children:
            child_data = child.data(0, Qt.ItemDataRole.UserRole) or {}
            if child_data.get("type") == "folder":
                self.discover_directory_branch(child, visited)

    def load_matching_service_layers(self, search_text, selected_category):
        """Load sublayers only for services whose name/path matches the query."""
        candidates = []
        for item in self.iter_tree_items():
            data = item.data(0, Qt.ItemDataRole.UserRole) or {}
            if (
                data.get("type") == "arcgis_service"
                and not data.get("is_loaded", False)
                and self.item_matches_search(item, search_text, selected_category)
            ):
                candidates.append(item)

        for item in candidates:
            self.load_dynamic_node(item)

    def perform_deep_search(self):
        """Discover unopened REST directories so their services are searchable."""
        if self._discovering_catalog:
            return

        search_text = self.normalize_search_text(self.search_input.text().strip())
        if not search_text:
            return

        if self._directory_catalog_loaded:
            self._discovering_catalog = True
            try:
                self.load_matching_service_layers(
                    search_text, self.category_combo.currentText()
                )
            finally:
                self._discovering_catalog = False
                self.filter_services()
            return

        from qgis.PyQt.QtWidgets import QApplication

        self._discovering_catalog = True
        self.iface.messageBar().pushMessage(
            "PeruSpatial Hub",
            "Explorando carpetas REST para completar la búsqueda...",
            level=0,
            duration=4,
        )
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        QApplication.processEvents()
        try:
            visited = set()
            for top_index in range(self.tree_widget.topLevelItemCount()):
                top_item = self.tree_widget.topLevelItem(top_index)
                for item in list(self.iter_tree_items(top_item)):
                    data = item.data(0, Qt.ItemDataRole.UserRole) or {}
                    if data.get("type") == "server":
                        self.discover_directory_branch(item, visited)

            self._directory_catalog_loaded = True
            self.load_matching_service_layers(
                search_text, self.category_combo.currentText()
            )
        finally:
            self._discovering_catalog = False
            QApplication.restoreOverrideCursor()
            self.filter_services()

    def on_selection_changed(self):
        """Loads metadata details when a service node is selected."""
        selected_items = self.tree_widget.selectedItems()
        if not selected_items:
            self.update_buttons_state(None)
            return

        item = selected_items[0]
        s = item.data(0, Qt.ItemDataRole.UserRole)
        
        self.update_buttons_state(s)

    def on_item_expanded(self, item):
        """Called when a tree node is expanded. Loads subfolders/services dynamically."""
        node_data = item.data(0, Qt.ItemDataRole.UserRole)
        if node_data and node_data.get("type") in ["server", "folder", "arcgis_service"] and not node_data.get("is_loaded", False):
            self.load_dynamic_node(item)

    def load_dynamic_node(self, item):
        node_data = item.data(0, Qt.ItemDataRole.UserRole)
        url = node_data["url"]
        stype = node_data["stype"]
        inst = node_data["institution"]
        cat = node_data["category"]

        from qgis.PyQt.QtWidgets import QApplication
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        
        item.takeChildren()
        loading_node = QTreeWidgetItem(item)
        loading_node.setText(0, "Cargando...")
        QApplication.processEvents()

        loaded_ok = False
        try:
            if stype == "arcgis_rest":
                data = self.fetch_arcgis_json(url)
                    
                # Folders
                for f in data.get("folders", []):
                    folder_name = f
                    furl = _append_rest_path(url, folder_name)

                    f_item = QTreeWidgetItem(item)
                    f_item.setText(0, folder_name)
                    f_item.setText(1, "Carpeta REST")
                    f_item.setFont(0, QFont("Segoe UI", 9, QFont.Weight.Bold))
                    f_item.setData(0, Qt.ItemDataRole.UserRole, {
                        "type": "folder",
                        "stype": "arcgis_rest",
                        "url": furl,
                        "is_loaded": False,
                        "name": folder_name,
                        "institution": inst,
                        "category": cat,
                    })
                    dummy = QTreeWidgetItem(f_item)
                    dummy.setText(0, "Expandir para explorar...")

                # Services
                for s in data.get("services", []):
                    sname = s.get("name")
                    stype_str = s.get("type")
                    if not sname or stype_str not in ("MapServer", "FeatureServer", "ImageServer"):
                        continue
                    
                    friendly_type = None
                    if stype_str == "MapServer":
                        friendly_type = "arcgis_mapserver"
                    elif stype_str == "FeatureServer":
                        friendly_type = "arcgisfeatureserver"
                    elif stype_str == "ImageServer":
                        friendly_type = "arcgis_imageserver"
                    
                    sname_short = sname.split('/')[-1]
                    surl = _service_url(url, sname, stype_str)
                    is_image = stype_str == "ImageServer"
                    
                    s_item = QTreeWidgetItem(item)
                    s_item.setText(0, sname_short)
                    s_item.setText(1, self.friendly_type(friendly_type))
                    s_item.setData(0, Qt.ItemDataRole.UserRole, {
                        "type": "arcgis_raster_layer" if is_image else "arcgis_service",
                        "stype": friendly_type,
                        "service_kind": stype_str,
                        "url": surl,
                        "name": sname_short,
                        "institution": inst,
                        "category": cat,
                        "description": f"Servicio REST {stype_str} en vivo provisto por {inst}.",
                        "is_loaded": is_image,
                    })
                    if not is_image:
                        dummy = QTreeWidgetItem(s_item)
                        dummy.setText(0, "Expandir para ver capas REST...")

                loaded_ok = True

            elif node_data.get("type") == "arcgis_service":
                data = self.fetch_arcgis_json(url)
                self.populate_arcgis_service_layers(item, node_data, data)
                loaded_ok = True

            else:
                raise RuntimeError(f"Tipo REST no compatible: {stype}")

        except Exception as e:
            error_node = QTreeWidgetItem(item)
            error_node.setText(0, f"Error al cargar: {str(e)}")
            error_node.setText(1, "Reintentar al expandir")
            error_node.setForeground(0, QColor("red"))
            
        finally:
            if loading_node.parent() is item:
                item.removeChild(loading_node)
            node_data["is_loaded"] = loaded_ok
            item.setData(0, Qt.ItemDataRole.UserRole, node_data)
            QApplication.restoreOverrideCursor()
            # Keep an active search consistent when a matching folder/service
            # is expanded and its nested layers are loaded on demand.
            if self.search_input.text().strip() and not self._discovering_catalog:
                self.filter_services()

    def populate_arcgis_service_layers(self, service_item, service_data, metadata):
        """Create importable leaf nodes for a MapServer or FeatureServer."""
        service_url = _clean_rest_url(service_data["url"])
        service_kind = service_data.get("service_kind") or self.service_kind_from_url(
            service_url, service_data.get("stype")
        )
        entries = []
        for layer_info in metadata.get("layers", []):
            entry = dict(layer_info)
            entry["is_table"] = False
            entries.append(entry)
        for table_info in metadata.get("tables", []):
            entry = dict(table_info)
            entry["is_table"] = True
            entries.append(entry)

        if not entries:
            raise RuntimeError("el servicio REST no publicó capas ni tablas importables")

        by_id = {entry.get("id"): entry for entry in entries if entry.get("id") is not None}
        created = {}

        def create_entry(entry):
            layer_id = entry.get("id")
            if layer_id in created:
                return created[layer_id]

            parent_item = service_item
            parent_id = entry.get("parentLayerId", -1)
            if parent_id in by_id and parent_id != layer_id:
                parent_item = create_entry(by_id[parent_id])

            layer_name = entry.get("name") or f"Capa {layer_id}"
            sublayer_ids = entry.get("subLayerIds")
            is_group = entry.get("type") == "Group Layer" or bool(sublayer_ids)
            tree_item = QTreeWidgetItem(parent_item)
            tree_item.setText(0, layer_name)

            if is_group:
                tree_item.setText(1, "Grupo REST")
                tree_item.setFont(0, QFont("Segoe UI", 9, QFont.Weight.Bold))
                tree_item.setData(0, Qt.ItemDataRole.UserRole, {
                    "type": "arcgis_group",
                    "stype": service_data["stype"],
                    "url": service_url,
                    "name": layer_name,
                    "institution": service_data["institution"],
                    "category": service_data["category"],
                    "description": "Grupo de subcapas del servicio ArcGIS REST.",
                })
            else:
                layer_type_name = str(entry.get("type", "")).casefold()
                has_geometry = bool(entry.get("geometryType"))
                is_vector = (
                    service_kind == "FeatureServer"
                    or entry.get("is_table", False)
                    or has_geometry
                )
                is_raster = "raster" in layer_type_name or "mosaic" in layer_type_name
                # MapServer vector sublayers keep the map-layer implementation so
                # importing can fall back to the rendered raster endpoint if needed.
                leaf_type = (
                    "arcgis_vector_layer"
                    if service_kind == "FeatureServer" or entry.get("is_table", False)
                    else "arcgis_map_layer"
                )
                layer_url = _append_rest_path(service_url, layer_id)
                if is_vector:
                    display_type = "Vectorial REST"
                    data_kind = "vectorial"
                elif is_raster:
                    display_type = "Raster REST"
                    data_kind = "raster"
                else:
                    display_type = "Raster/Vectorial REST"
                    data_kind = "mixto"
                tree_item.setText(1, display_type)
                tree_item.setData(0, Qt.ItemDataRole.UserRole, {
                    "type": leaf_type,
                    "stype": leaf_type,
                    "data_kind": data_kind,
                    "service_kind": service_kind,
                    "service_url": service_url,
                    "url": layer_url,
                    "layer_id": layer_id,
                    "name": layer_name,
                    "institution": service_data["institution"],
                    "category": service_data["category"],
                    "description": f"Capa {layer_id} del servicio ArcGIS REST {service_kind}.",
                    "crs_warning": service_data.get("crs_warning", False),
                })
            created[layer_id] = tree_item
            return tree_item

        for entry in entries:
            create_entry(entry)

    def on_item_double_clicked(self, item, column):
        """Expand REST containers or add an individual REST layer."""
        s = item.data(0, Qt.ItemDataRole.UserRole)
        if s is None:
            return
        if s.get("type") in ["server", "folder", "arcgis_service", "arcgis_group", "ogc_service"]:
            item.setExpanded(not item.isExpanded())
        else:
            self.add_selected_layer()

    def update_buttons_state(self, s):
        """Enables/disables buttons and sets metadata description based on selection."""
        if s is None:
            self.metadata_panel.setHtml(
                "<p style='color: #666;'>Seleccione un servicio del catálogo superior para ver su descripción "
                "y realizar operaciones.</p>"
            )
            self.crs_banner.setStyleSheet("""
                QLabel {
                    background-color: #fff2cc;
                    border: 1px solid #ffe599;
                    color: #7f6000;
                    padding: 6px;
                    border-radius: 4px;
                    font-size: 10.5px;
                }
            """)
            self.crs_banner.setText(
                "<b>💡 Nota de Precisión (Geofísica/Arqueología):</b><br>"
                "Los levantamientos de precisión requieren el datum correcto. Asegúrese de "
                "configurar su proyecto QGIS en el huso UTM adecuado (ej. <b>WGS84 / UTM 18S</b> - EPSG:32718). "
                "Si usa capas históricas en <b>PSAD56</b>, aplique la transformación a WGS84 para evitar desfases."
            )
            self.btn_add_layer.setEnabled(False)
            self.btn_register_browser.setEnabled(False)
            self.btn_copy_url.setEnabled(False)
            self.btn_open_browser.setEnabled(False)
        else:
            ntype = s.get("type", "service")
            crs_advisory = ""
            if s.get("crs_warning", False):
                crs_advisory = (
                    "<div style='background-color: #f8cecc; border: 1px solid #b85450; color: #a20000; "
                    "padding: 8px; border-radius: 4px; margin-top: 10px;'>"
                    "<b>⚠️ ADVERTENCIA DE CRS / DATUM:</b><br>"
                    "Este servicio contiene capas históricas o de arqueología que tradicionalmente operan en "
                    "<b>PSAD56</b>. Al integrarlas en un proyecto <b>WGS84 / SIRGAS UTM</b>, asegúrese de aplicar "
                    "la transformación de datum oficial de IGN/MINCUL para evitar desplazamientos de hasta 200 metros."
                    "</div>"
                )
                self.crs_banner.setStyleSheet("""
                    QLabel {
                        background-color: #f8cecc;
                        border: 1px solid #b85450;
                        color: #a20000;
                        padding: 6px;
                        border-radius: 4px;
                        font-size: 10.5px;
                    }
                """)
                self.crs_banner.setText(
                    "<b>⚠️ Advertencia de Precisión:</b> Capas arqueológicas/históricas en PSAD56 detectadas. "
                    "¡No asuma WGS84 automáticamente! Transforme la capa para evitar desfases métricos en su retícula."
                )
            else:
                self.crs_banner.setStyleSheet("""
                    QLabel {
                        background-color: #d5e8d4;
                        border: 1px solid #82b366;
                        color: #274e13;
                        padding: 6px;
                        border-radius: 4px;
                        font-size: 10.5px;
                    }
                """)
                self.crs_banner.setText(
                    "<b>✅ Datum Moderno Compatible:</b> Este servicio opera en WGS84 / SIRGAS UTM de forma nativa. "
                    "Se alinea perfectamente con mapas base de satélite y coordenadas de GPS modernas."
                )

            tags_html = "".join([f"<span style='background-color: #e1e1e1; padding: 2px 6px; margin-right: 4px; border-radius: 3px; font-size: 10px;'>{tag}</span>" for tag in s.get("tags", [])])

            if ntype == "ogc_service":
                html = f"""
                    <h3>{s['name']}</h3>
                    <p><b>Institución:</b> {s['institution']}</p>
                    <p><b>Categoría:</b> {s['category']}</p>
                    <p><b>Tipo:</b> Servicio WMS oficial verificado</p>
                    <p><b>Descripción:</b> Registre esta conexión para explorar sus capas desde la sección WMS/WMTS del panel Explorador de QGIS.</p>
                    <p><b>URL del Servidor:</b><br><a href='{s['url']}'>{s['url']}</a></p>
                """
                self.metadata_panel.setHtml(html)
                self.btn_add_layer.setEnabled(False)
                self.btn_register_browser.setEnabled(True)
                self.btn_copy_url.setEnabled(True)
                self.btn_open_browser.setEnabled(True)
            elif ntype in ["server", "folder", "arcgis_service", "arcgis_group"]:
                html = f"""
                    <h3>{s['name']}</h3>
                    <p><b>Institución:</b> {s['institution']}</p>
                    <p><b>Categoría:</b> {s['category']}</p>
                    <p><b>Tipo:</b> Directorio de Servidor ({s['stype']})</p>
                    <p><b>Descripción:</b> Directorio en vivo del servidor del estado peruano. Expanda este nodo en el catálogo superior para explorar dinámicamente todas sus subcarpetas y servicios publicados en tiempo real.</p>
                    <p><b>URL del Servidor:</b><br><a href='{s['url']}'>{s['url']}</a></p>
                """
                self.metadata_panel.setHtml(html)
                self.btn_add_layer.setEnabled(False)
                self.btn_register_browser.setEnabled(ntype != "arcgis_group")
                self.btn_copy_url.setEnabled(True)
                self.btn_open_browser.setEnabled(True)
            else:
                friendly_t = self.friendly_type(s['stype'])
                html = f"""
                    <h3>{s['name']}</h3>
                    <p><b>Institución:</b> {s['institution']}</p>
                    <p><b>Categoría:</b> {s['category']}</p>
                    <p><b>Tipo de Conexión:</b> {friendly_t}</p>
                    <p><b>Descripción:</b> {s.get('description', '')}</p>
                    <p><b>URL del Servicio:</b><br><a href='{s['url']}'>{s['url']}</a></p>
                    <p><b>Etiquetas:</b> {tags_html}</p>
                    {crs_advisory}
                """
                self.metadata_panel.setHtml(html)
                self.btn_add_layer.setEnabled(True)
                self.btn_register_browser.setEnabled(True)
                self.btn_copy_url.setEnabled(True)
                self.btn_open_browser.setEnabled(True)

    @staticmethod
    def provider_error(layer):
        if layer is None:
            return "QGIS no creó la capa"
        try:
            summary = layer.error().summary()
            if summary:
                return summary
        except Exception:
            return "el proveedor QGIS no devolvió detalles del error REST"
        return "el proveedor QGIS consideró inválida la fuente ArcGIS REST"

    @staticmethod
    def apply_metadata_crs(layer, metadata):
        if not layer or not layer.isValid() or layer.crs().isValid():
            return
        extent = metadata.get("extent") or metadata.get("fullExtent") or {}
        spatial_ref = metadata.get("spatialReference") or extent.get("spatialReference") or {}
        wkid = spatial_ref.get("latestWkid") or spatial_ref.get("wkid")
        if not wkid:
            return
        crs = QgsCoordinateReferenceSystem.fromEpsgId(int(wkid))
        if not crs.isValid():
            crs = QgsCoordinateReferenceSystem(f"ESRI:{wkid}")
        if crs.isValid():
            layer.setCrs(crs)

    def create_arcgis_vector_layer(self, layer_url, name, metadata=None):
        uri = QgsDataSourceUri()
        uri.setParam("url", _clean_rest_url(layer_url))
        layer = QgsVectorLayer(uri.uri(False), name, "arcgisfeatureserver")
        self.apply_metadata_crs(layer, metadata or {})
        return layer

    def create_arcgis_map_layer(self, service_url, layer_id, name, metadata=None):
        uri = QgsDataSourceUri()
        uri.setParam("url", _clean_rest_url(service_url))
        uri.setParam("layer", str(layer_id))
        uri.setParam("format", "png32")
        layer = QgsRasterLayer(uri.uri(False), name, "arcgismapserver")
        self.apply_metadata_crs(layer, metadata or {})
        return layer

    def create_arcgis_image_layer(self, url, name, metadata=None):
        uri = QgsDataSourceUri()
        uri.setParam("url", _clean_rest_url(url))
        layer = QgsRasterLayer(uri.uri(False), name, "arcgisimageserver")
        if not layer.isValid():
            layer = QgsRasterLayer(uri.uri(False), name, "arcgismapserver")
        self.apply_metadata_crs(layer, metadata or {})
        return layer

    def add_selected_layer(self):
        """Add one native vector or raster layer from an ArcGIS REST endpoint."""
        selected_items = self.tree_widget.selectedItems()
        if not selected_items:
            return

        s = selected_items[0].data(0, Qt.ItemDataRole.UserRole)
        if not s or s.get("type") in ["server", "folder", "arcgis_service", "arcgis_group", "ogc_service"]:
            return

        from qgis.PyQt.QtWidgets import QApplication
        name = s["name"]
        layer_type = s.get("type")
        attempts = []
        layer = None
        metadata = {}

        self.iface.messageBar().pushMessage(
            "PeruSpatial Hub", f"Consultando capa REST: {name}...", level=0, duration=2
        )
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        QApplication.processEvents()
        try:
            if layer_type == "arcgis_vector_layer":
                layer = self.create_arcgis_vector_layer(s["url"], name)
                if not layer.isValid():
                    attempts.append(f"Vector REST: {self.provider_error(layer)}")

            elif layer_type == "arcgis_map_layer":
                try:
                    metadata = self.fetch_arcgis_json(s["url"], timeout=12)
                except Exception as exc:
                    attempts.append(f"Metadatos REST: {exc}")

                geometry_type = metadata.get("geometryType")
                layer_kind = str(metadata.get("type", "")).lower()
                capabilities = str(metadata.get("capabilities", "")).lower()
                queryable_vector = bool(geometry_type) and (
                    not capabilities or "query" in capabilities
                ) and "raster" not in layer_kind

                if queryable_vector:
                    layer = self.create_arcgis_vector_layer(s["url"], name, metadata)
                    if not layer.isValid():
                        attempts.append(f"Vector REST: {self.provider_error(layer)}")

                if not layer or not layer.isValid():
                    layer = self.create_arcgis_map_layer(
                        s["service_url"], s["layer_id"], name, metadata
                    )
                    if not layer.isValid():
                        attempts.append(f"Raster MapServer: {self.provider_error(layer)}")

            elif layer_type == "arcgis_raster_layer" or s.get("service_kind") == "ImageServer":
                try:
                    metadata = self.fetch_arcgis_json(s["url"], timeout=12)
                except Exception as exc:
                    attempts.append(f"Metadatos REST: {exc}")
                layer = self.create_arcgis_image_layer(s["url"], name, metadata)
                if not layer.isValid():
                    attempts.append(f"Raster ImageServer: {self.provider_error(layer)}")

            else:
                attempts.append(f"Tipo no importable: {layer_type}")

            if layer and layer.isValid():
                QgsProject.instance().addMapLayer(layer)
                data_kind = "vectorial" if isinstance(layer, QgsVectorLayer) else "raster"
                self.iface.messageBar().pushMessage(
                    "PeruSpatial Hub",
                    f"Capa {data_kind} REST '{name}' añadida correctamente.",
                    level=3,
                    duration=4,
                )
                return
        except Exception as exc:
            attempts.append(str(exc))
        finally:
            QApplication.restoreOverrideCursor()

        detail = "\n".join(f"- {message}" for message in attempts) or "- Error desconocido"
        QMessageBox.warning(
            self,
            "Error al importar ArcGIS REST",
            f"No se pudo cargar la capa '{name}'.\n\n{detail}\n\n"
            "La capa no se intentó cargar mediante WMS.",
        )

    def register_selected_connection(self):
        """Registers the selected service in QGIS Settings for Browser panel integration."""
        selected_items = self.tree_widget.selectedItems()
        if not selected_items:
            return
        
        s = selected_items[0].data(0, Qt.ItemDataRole.UserRole)
        if s is None:
            return

        name = s["name"]
        url = s.get("service_url", s["url"])
        stype = s.get("stype", s.get("type"))
        if stype in ["arcgis_map_layer", "arcgis_raster_layer", "arcgis_imageserver"]:
            stype = "arcgis_mapserver"
        elif stype == "arcgis_vector_layer":
            stype = (
                "arcgisfeatureserver"
                if s.get("service_kind") == "FeatureServer"
                else "arcgis_mapserver"
            )

        self.write_connection(name, url, stype)

        connection_section = "WMS/WMTS" if stype == "wms" else "ArcGIS REST"

        QMessageBox.information(
            self,
            "Conexión Registrada",
            f"La conexión '{name}' ha sido agregada con éxito al panel Explorador de QGIS.\n\n"
            f"Puede encontrarla en la sección nativa {connection_section}."
        )

    def register_all_connections(self):
        """Registers all database services in QGIS Settings at once."""
        reply = QMessageBox.question(
            self,
            "Registrar Todos los Servicios",
            "¿Desea registrar todas las conexiones verificadas del catálogo en el panel Explorador de QGIS?\n\n"
            "Esto creará conexiones nativas organizadas para que pueda explorar todo el catálogo del estado "
            "peruano directamente desde el panel de QGIS.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )

        if reply == QMessageBox.StandardButton.Yes:
            count = 0
            for s in self.live_servers:
                full_name = f"{s['institution']} - {s['name']}"
                self.write_connection(full_name, s["url"], s["stype"])
                count += 1
            
            self.iface.reloadConnections()

            QMessageBox.information(
                self,
                "Registro Completo",
                f"Se han registrado {count} conexiones en el panel Explorador de QGIS.\n\n"
                "Revise las secciones 'ArcGIS REST Servers' y 'WMS/WMTS' del panel Explorador."
            )

    def write_connection(self, name, url, stype):
        """Writes the actual connection settings to QSettings."""
        settings = QgsSettings()
        
        if stype in ["arcgis_mapserver", "arcgisfeatureserver", "arcgis_imageserver", "arcgis_rest"]:
            if stype == "arcgisfeatureserver":
                key = f"qgis/connections-arcgisfeatureserver/{name}/"
            else:
                key = f"qgis/connections-arcgismapserver/{name}/"
            
            settings.setValue(key + "url", url)
            settings.setValue(key + "authcfg", "")
        elif stype == "wms":
            key = f"qgis/connections-wms/{name}/"
            settings.setValue(key + "url", url)
            settings.setValue(key + "authcfg", "")
        self.iface.reloadConnections()

    def copy_selected_url(self):
        """Copies the URL of the selected service to the clipboard."""
        selected_items = self.tree_widget.selectedItems()
        if not selected_items:
            return
        
        s = selected_items[0].data(0, Qt.ItemDataRole.UserRole)
        if s is not None:
            clipboard = self.iface.mainWindow().clipboard()
            clipboard.setText(s["url"])
            self.iface.messageBar().pushMessage(
                "PeruSpatial Hub",
                "URL copiada al portapapeles.",
                level=3, # Success
                duration=2
            )

    def open_selected_web(self):
        """Opens the selected service's REST/WMS endpoint page in default web browser."""
        selected_items = self.tree_widget.selectedItems()
        if not selected_items:
            return
        
        s = selected_items[0].data(0, Qt.ItemDataRole.UserRole)
        if s is not None:
            webbrowser.open(s["url"])
