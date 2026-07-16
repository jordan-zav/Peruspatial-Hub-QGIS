# PeruSpatial Hub - QGIS Plugin

Versión estable: 1.0.0

**PeruSpatial Hub** es un plugin para QGIS diseñado para centralizar y facilitar el acceso a la Infraestructura de Datos Espaciales (IDE) de las principales instituciones públicas del Perú. 

Este plugin es una herramienta indispensable para profesionales en **arqueología, geofísica, ingeniería y exploración minera**, ya que permite explorar e integrar de forma inmediata la cartografía base y temática del país.

## Licencia de código abierto

PeruSpatial Hub se distribuye bajo la GNU General Public License v3.0. Puede usar, estudiar, modificar y redistribuir el código de acuerdo con los términos incluidos en el archivo LICENSE.

---

## 🚀 Características Principales

1. **Catálogo Unificado**: Más de 40 servicios GIS precargados y clasificados por institución y temática (Catastro, Minería, Hidrografía, Medio Ambiente, Riesgos, Arqueología).
2. **Buscador Inteligente**: Filtra en tiempo real por palabras clave (ej: "sismos", "concesiones", "cuencas") y por categoría.
3. **Carga Inmediata**: Haz doble clic en cualquier servicio del catálogo para añadirlo al lienzo de mapas de QGIS (soporta ArcGIS MapServer, FeatureServer, WMS y WFS).
4. **Integración con el Explorador de QGIS**: Registra de forma individual o masiva todas las conexiones oficiales del catálogo directamente en el panel **Explorador** nativo de QGIS (bajo las categorías WMS/WMTS y ArcGIS REST).
5. **Asistente de Precisión de CRS / Datum**: Panel de advertencia dinámico que le guiará para evitar errores al trabajar con datums mixtos (especialmente la transformación del datum histórico **PSAD56** al moderno **WGS84 / SIRGAS UTM**), garantizando la precisión métrica obligatoria en trabajos arqueológicos y geofísicos.

---

## 📂 Servidores de Información Integrados

*   **INGEMMET (GEOCATMIN)**: Catastro minero, atlas geoquímico, volcanes, peligros geológicos, aeromagnetometría geofísica regional.
*   **IGN (Instituto Geográfico Nacional)**: Límites departamentales/provinciales/distritales, red de vías, hidrografía nacional y toponimia a escala 1:100,000.
*   **ANA (Autoridad Nacional del Agua)**: Delimitación de unidades hidrográficas (cuencas), red de ríos, inventario de lagunas y glaciares.
*   **IGP (Instituto Geofísico del Perú)**: Sismos históricos y fallas activas.
*   **MINAM y SERNANP**: Áreas Naturales Protegidas (ANP), zonas de amortiguamiento, ecosistemas y Zonificación Ecológica Económica (ZEE).
*   **SERFOR**: Cobertura forestal y concesiones madereras.
*   **MINCUL (Ministerio de Cultura)**: Monumentos y zonas arqueológicas, áreas CIRA declaradas Patrimonio Cultural de la Nación.
*   **CENEPRED**: Mapas de susceptibilidad a inundaciones y movimientos en masa (huaicos).
*   **SUNARP y COFOPRI**: Consulta catastral de predios y sectores urbanos.
*   **OSINERGMIN**: Líneas de transmisión eléctrica, oleoductos y gasoductos.
*   **OEFA**: Monitoreo de calidad ambiental y pasivos ambientales.

---

## 🛠️ Instalación Manual

Dado que el plugin está en desarrollo activo, puede instalarlo manualmente siguiendo estos pasos:

1. Localice la carpeta de plugins de su perfil de QGIS. Normalmente se encuentra en:
   * **Windows**: C:\Users\TuUsuario\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\
   * **Linux**: ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/
   * **macOS**: /Users/TuUsuario/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/
2. Copie la carpeta completa peruspatial_hub dentro del directorio plugins anterior.
3. Abra QGIS, vaya al menú superior **Complementos** > **Administrar e instalar complementos...**
4. Busque **PeruSpatial Hub** en la sección "Instalados" y active la casilla correspondiente.
5. Verá un nuevo ícono de globo/base de datos en la barra de herramientas "Base de datos" y una opción en el menú **Base de datos** > **PeruSpatial Hub** para abrir el panel.

---

## ⚠️ Reglas Críticas de Precisión Espacial (Datum y CRS)

Si está trabajando con datos arqueológicos o geofísicos en el Perú, siga rigurosamente estas reglas:

*   **No asuma WGS84 como único datum**: Las capas antiguas y planos arqueológicos heredados suelen estar en **PSAD56 (Provisional South American 1956)**. Si simplemente "define" la proyección como WGS84, sufrirá un **desfase de hasta 200 metros** en el terreno.
*   **Use transformaciones de datum oficiales**: Al importar datos de instituciones como el Ministerio de Cultura en PSAD56, aplique siempre herramientas de reproyección utilizando los coeficientes oficiales de transformación hacia WGS84/SIRGAS.
*   **Mantenga un CRS Maestro de Proyecto**: Realice el procesamiento geofísico y mapeo en un único CRS proyectado (generalmente UTM Huso 17S, 18S o 19S dependiendo de la ubicación regional en el Perú).

## Soporte y código fuente

Desarrollado por [Jordan Zavaleta](https://gisgeo.dev).

El código fuente y el seguimiento de incidencias se encuentran en [GitHub](https://github.com/jordan-zav/peruspatial-hub-qgis).
