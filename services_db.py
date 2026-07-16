# -*- coding: utf-8 -*-
"""
Database of curated Peruvian geospatial services for PeruSpatial Hub.
"""

SERVICES = [
    # --- INGEMMET (GEOCATMIN) ---
    {
        "institution": "INGEMMET (GEOCATMIN)",
        "name": "Catastro Minero Nacional (WGS84)",
        "url": "https://geocatmin.ingemmet.gob.pe/arcgis/rest/services/SERV_CATASTRO_MINERO_WGS84/MapServer",
        "type": "arcgis_mapserver",
        "category": "Geología y Minería",
        "description": "Servicio de Catastro Minero Oficial del Perú referenciado al datum WGS84. Contiene concesiones mineras otorgadas, en trámite, extinguidas y áreas de no admisión de petitorios.",
        "crs_warning": False,
        "tags": ["concesiones", "catastro", "minero", "derechos", "petitorios", "ingemmet"]
    },
    {
        "institution": "INGEMMET (GEOCATMIN)",
        "name": "Atlas Geoquímico Nacional",
        "url": "https://geocatmin.ingemmet.gob.pe/arcgis/rest/services/SERV_ATLAS_GEOQUIMICO/MapServer",
        "type": "arcgis_mapserver",
        "category": "Geología y Minería",
        "description": "Distribución geoquímica multielemental de muestras de sedimentos de corriente a nivel nacional. Útil para exploración minera e identificación de anomalías.",
        "crs_warning": False,
        "tags": ["geoquimica", "sedimentos", "anomalias", "muestras", "ingemmet"]
    },
    {
        "institution": "INGEMMET (GEOCATMIN)",
        "name": "Potencial Minero",
        "url": "https://geocatmin.ingemmet.gob.pe/arcgis/rest/services/SERV_POTENCIALMINERO/MapServer",
        "type": "arcgis_mapserver",
        "category": "Geología y Minería",
        "description": "Información sobre recursos, reservas, potencial metálico y no metálico, prospectos mineros y proyectos geológicos.",
        "crs_warning": False,
        "tags": ["potencial", "recursos", "reservas", "metalico", "prospectos", "ingemmet"]
    },
    {
        "institution": "INGEMMET (GEOCATMIN)",
        "name": "Peligros Volcánicos y Volcanes",
        "url": "https://geocatmin.ingemmet.gob.pe/arcgis/rest/services/SERV_VOLCANES/MapServer",
        "type": "arcgis_mapserver",
        "category": "Clima y Riesgos",
        "description": "Ubicación de volcanes activos y potencialmente activos en el sur del Perú, mapas de peligros por caídas de ceniza, lahares y flujos piroclásticos.",
        "crs_warning": False,
        "tags": ["volcanes", "peligros", "lahares", "cenizas", "monitoreo", "ingemmet"]
    },
    {
        "institution": "INGEMMET (GEOCATMIN)",
        "name": "Peligros Geológicos y Susceptibilidad",
        "url": "https://geocatmin.ingemmet.gob.pe/arcgis/rest/services/SERV_PELIGROS_GEOLOGICOS/MapServer",
        "type": "arcgis_mapserver",
        "category": "Clima y Riesgos",
        "description": "Zonas susceptibles a movimientos en masa, deslizamientos, derrumbes, inundaciones y fallas geológicas activas.",
        "crs_warning": False,
        "tags": ["peligros", "deslizamientos", "derrumbes", "riesgos", "huaicos", "ingemmet"]
    },
    {
        "institution": "INGEMMET (GEOCATMIN)",
        "name": "Paleontología (Fósiles)",
        "url": "https://geocatmin.ingemmet.gob.pe/arcgis/rest/services/SERV_PALEONTOLOGIA/MapServer",
        "type": "arcgis_mapserver",
        "category": "Geología y Minería",
        "description": "Ubicación de zonas paleontológicas, inventario de fósiles oficiales del Perú y muestras recolectadas.",
        "crs_warning": False,
        "tags": ["fosiles", "paleontologia", "muestras", "ingemmet"]
    },
    {
        "institution": "INGEMMET (GEOCATMIN)",
        "name": "Aeromagnetometría (Magnetismo)",
        "url": "https://geocatmin.ingemmet.gob.pe/arcgis/rest/services/SERV_AEROMAGNETIICO/ImageServer",
        "type": "arcgis_mapserver",
        "category": "Geología y Minería",
        "description": "Servicio de imágenes geofísicas aéreas (aeromagnetometría). Muestra anomalías magnéticas del subsuelo nacional, esencial para prospección geofísica regional.",
        "crs_warning": False,
        "tags": ["aeromagnetico", "geofisica", "magnetometria", "anomalias", "ingemmet"]
    },
    {
        "institution": "INGEMMET (GEOCATMIN)",
        "name": "Zonas Geológicas e IA WGS84",
        "url": "https://geocatmin.ingemmet.gob.pe/arcgis/rest/services/WEBGIS_ZONAS_GEOWGS84/FeatureServer",
        "type": "arcgisfeatureserver",
        "category": "Geología y Minería",
        "description": "Servicio de entidades (FeatureServer) que permite consultas y descargas vectoriales de geología regional, fallas, prospectividad con Inteligencia Artificial.",
        "crs_warning": False,
        "tags": ["vector", "features", "geologia", "inteligencia artificial", "ingemmet"]
    },
    {
        "institution": "INGEMMET (GEOCATMIN)",
        "name": "Cartera de Proyectos Mineros",
        "url": "https://geocatmin.ingemmet.gob.pe/arcgis/rest/services/SERV_CARTERA_PROYECTOS_MINEROS/MapServer",
        "type": "arcgis_mapserver",
        "category": "Geología y Minería",
        "description": "Localización y datos clave de proyectos mineros en fases de exploración y explotación a nivel nacional.",
        "crs_warning": False,
        "tags": ["proyectos", "inversion", "exploracion", "explotacion", "ingemmet"]
    },
    {
        "institution": "INGEMMET (GEOCATMIN)",
        "name": "Pasivos Ambientales Mineros",
        "url": "https://geocatmin.ingemmet.gob.pe/arcgis/rest/services/SERV_PASIVAS_AMBIENTALES/MapServer",
        "type": "arcgis_mapserver",
        "category": "Medio Ambiente",
        "description": "Inventario nacional de pasivos ambientales generados por actividades mineras históricas inactivas.",
        "crs_warning": False,
        "tags": ["pasivos", "mineria", "contaminacion", "ochoa", "ingemmet"]
    },
    {
        "institution": "INGEMMET (GEOCATMIN)",
        "name": "Servicio OGC Integrado (WMS)",
        "url": "https://geocatmin.ingemmet.gob.pe/arcgis/services/Servicios_OGC/OGC_Geocatmin/MapServer/WMSServer",
        "type": "wms",
        "category": "Geología y Minería",
        "description": "Servicio de mapas web (WMS) que agrupa múltiples capas de GEOCATMIN: geología, catastro minero, sismología y peligros en formato estándar OGC.",
        "crs_warning": False,
        "tags": ["wms", "ogc", "geocatmin", "concesiones", "ingemmet"]
    },

    # --- GEOCATMIN ANTIGUO (HISTÓRICO) ---
    {
        "institution": "GEOCATMIN Antiguo",
        "name": "Catastro Minero Histórico",
        "url": "https://geocatminapp.ingemmet.gob.pe/arcgis/rest/services/SERV_CATASTRO_MINERO/MapServer",
        "type": "arcgis_mapserver",
        "category": "Geología y Minería",
        "description": "Servidor secundario de INGEMMET que contiene catastros históricos o en versiones previas de delimitaciones territoriales. ¡Atención con los datums!",
        "crs_warning": True,
        "tags": ["historico", "antiguo", "catastro", "ingemmet"]
    },

    # --- IDEP (INFRAESTRUCTURA DE DATOS ESPACIALES DEL PERÚ) ---
    {
        "institution": "IDEP",
        "name": "IGN Hidrografía 100K",
        "url": "https://www.idep.gob.pe/geoportal/rest/services/SERVICIOS_IGN/HIDROGRAFIA_100K/MapServer",
        "type": "arcgis_mapserver",
        "category": "Hidrología y Agua",
        "description": "Red hidrográfica oficial de la Carta Nacional a escala 1:100,000, provista por el IGN a través de la IDEP.",
        "crs_warning": False,
        "tags": ["rios", "lagos", "quebradas", "hidrografia", "ign", "idep"]
    },
    {
        "institution": "IDEP",
        "name": "IGN Límites Políticos 100K",
        "url": "https://www.idep.gob.pe/geoportal/rest/services/SERVICIOS_IGN/LIMITES_100K/MapServer",
        "type": "arcgis_mapserver",
        "category": "Límites y Cartografía",
        "description": "Límites departamentales, provinciales y distritales oficiales del Perú generados por el IGN a escala 1:100,000.",
        "crs_warning": False,
        "tags": ["limites", "departamentos", "provincias", "distritos", "politico", "ign", "idep"]
    },
    {
        "institution": "IDEP",
        "name": "IGN Vías y Transporte 100K",
        "url": "https://www.idep.gob.pe/geoportal/rest/services/SERVICIOS_IGN/VIAS_100K/MapServer",
        "type": "arcgis_mapserver",
        "category": "Límites y Cartografía",
        "description": "Red de carreteras, vías férreas y aeropuertos oficiales de la Carta Nacional 1:100,000.",
        "crs_warning": False,
        "tags": ["carreteras", "vias", "transporte", "caminos", "ign", "idep"]
    },
    {
        "institution": "IDEP",
        "name": "IGN Toponimia Oficial 100K",
        "url": "https://www.idep.gob.pe/geoportal/rest/services/SERVICIOS_IGN/TOPONIMIA_100K/MapServer",
        "type": "arcgis_mapserver",
        "category": "Límites y Cartografía",
        "description": "Toponimia y nombres oficiales de centros poblados, cerros, ríos y puntos geográficos de interés del IGN.",
        "crs_warning": False,
        "tags": ["nombres", "toponimia", "centros poblados", "ign", "idep"]
    },
    {
        "institution": "IDEP",
        "name": "MTC Infraestructura Institucional",
        "url": "https://www.idep.gob.pe/geoportal/rest/services/INSTITUCIONALES/MTC/MapServer",
        "type": "arcgis_mapserver",
        "category": "Límites y Cartografía",
 "description": "Infraestructura de transportes y comunicaciones a nivel nacional provista por el Ministerio de Transportes y Comunicaciones (MTC).",
        "crs_warning": False,
 "tags": ["puertos", "red vial", "puentes", "antenas", "mtc", "idep"]
    },

    # --- SENAMHI ---
    {
        "institution": "SENAMHI",
        "name": "Zonificación Climática e Isotermas",
        "url": "https://geoportal.senamhi.gob.pe/arcgis/rest/services/Clima/Temperaturas/MapServer",
        "type": "arcgis_mapserver",
        "category": "Clima y Riesgos",
        "description": "Mapas climáticos de temperaturas medias, máximas e isotermas a nivel nacional.",
        "crs_warning": False,
        "tags": ["temperatura", "clima", "isotermas", "calor", "frio", "senamhi"]
    },
    {
        "institution": "SENAMHI",
        "name": "Precipitación Media Anual",
        "url": "https://geoportal.senamhi.gob.pe/arcgis/rest/services/Clima/Precipitaciones/MapServer",
        "type": "arcgis_mapserver",
        "category": "Clima y Riesgos",
        "description": "Distribución espacial de lluvias, mapas de isoyetas e histórico de precipitaciones pluviales.",
        "crs_warning": False,
        "tags": ["lluvia", "isoyetas", "precipitacion", "clima", "senamhi"]
    },

    # --- IGP (INSTITUTO GEOFÍSICO DEL PERÚ) ---
    {
        "institution": "IGP",
        "name": "Sismos, Fallas y Vulcanología (WMS)",
        "url": "https://ide.igp.gob.pe/geoserver/ows?service=wms&version=1.3.0&request=GetCapabilities",
        "type": "wms",
        "category": "Clima y Riesgos",
        "description": "Servidor OGC de IGP. Ofrece sismos históricos registrados, fallas geológicas activas, zonificación sísmica y estaciones de monitoreo sísmico.",
        "crs_warning": False,
        "tags": ["sismos", "terremotos", "fallas", "geofisica", "wms", "igp"]
    },

    # --- SERNANP (ÁREAS NATURALES PROTEGIDAS) ---
    {
        "institution": "SERNANP",
        "name": "Áreas Naturales Protegidas (ANP)",
        "url": "http://geoservicios.sernanp.gob.pe/arcgis/rest/services/sial/sernanp/MapServer",
        "type": "arcgis_mapserver",
        "category": "Medio Ambiente",
        "description": "Áreas Naturales Protegidas de administración nacional (Parques, Reservas, Santuarios), regional y privadas oficiales.",
        "crs_warning": False,
        "tags": ["anp", "reservas", "parques nacionales", "conservacion", "sernanp"]
    },
    {
        "institution": "SERNANP",
        "name": "Zonas de Amortiguamiento",
        "url": "http://geoservicios.sernanp.gob.pe/arcgis/rest/services/sial/zonas_amortiguamiento/MapServer",
        "type": "arcgis_mapserver",
        "category": "Medio Ambiente",
        "description": "Zonas adyacentes a las Áreas Naturales Protegidas que requieren tratamiento especial para garantizar la conservación del área núcleo.",
        "crs_warning": False,
        "tags": ["amortiguamiento", "zonas", "sernanp", "conservacion"]
    },
    {
        "institution": "SERNANP",
        "name": "Servicio OGC de Áreas Protegidas (WMS)",
        "url": "http://geoservicios.sernanp.gob.pe/arcgis/services/sial/sernanp/MapServer/WMSServer",
        "type": "wms",
        "category": "Medio Ambiente",
        "description": "Acceso WMS estándar de SERNANP para visualizar las capas de áreas protegidas y zonas reservadas.",
        "crs_warning": False,
        "tags": ["anp", "wms", "ogc", "sernanp"]
    },

    # --- SERFOR (FORESTAL) ---
    {
        "institution": "SERFOR",
        "name": "Cobertura Forestal y Pérdida de Bosques",
        "url": "https://geoservicios.serfor.gob.pe/arcgis/rest/services/Cobertura_Forestal/MapServer",
        "type": "arcgis_mapserver",
        "category": "Medio Ambiente",
        "description": "Cobertura vegetal, tipos de bosques, zonas de deforestación y pérdida de bosques húmedos amazónicos.",
        "crs_warning": False,
        "tags": ["bosques", "deforestacion", "selva", "vegetacion", "serfor"]
    },
    {
        "institution": "SERFOR",
        "name": "Concesiones y Títulos Habilitantes",
        "url": "https://geoservicios.serfor.gob.pe/arcgis/rest/services/Concesiones/MapServer",
        "type": "arcgis_mapserver",
        "category": "Medio Ambiente",
        "description": "Concesiones forestales (madera y no maderables), contratos de conservación y permisos forestales.",
        "crs_warning": False,
        "tags": ["concesiones", "madera", "forestal", "contratos", "serfor"]
    },

    # --- MIDAGRI ---
    {
        "institution": "MIDAGRI",
        "name": "Estudios de Suelos y Tierras",
        "url": "https://siea.midagri.gob.pe/arcgis/rest/services/Suelos_Tierras/MapServer",
        "type": "arcgis_mapserver",
        "category": "Catastro y Propiedad",
        "description": "Clasificación de suelos, capacidad de uso mayor de la tierra, aptitud agrícola e irrigaciones del Perú.",
        "crs_warning": False,
        "tags": ["suelos", "agricultura", "riego", "tierras", "midagri", "siea"]
    },

    # --- CENEPRED (PREVENCIÓN DE RIESGOS) ---
    {
        "institution": "CENEPRED",
        "name": "Riesgo por Inundación (SIGRID)",
        "url": "https://sigrid.cenepred.gob.pe/arcgis/rest/services/Peligros/Susceptibilidad_Inundaciones/MapServer",
        "type": "arcgis_mapserver",
        "category": "Clima y Riesgos",
        "description": "Capas del Sistema de Información para la Gestión del Riesgo de Desastres (SIGRID) que delimitan zonas con alta susceptibilidad a inundaciones.",
        "crs_warning": False,
        "tags": ["inundaciones", "peligros", "riesgos", "sigrid", "cenepred"]
    },
    {
        "institution": "CENEPRED",
        "name": "Riesgo por Movimiento en Masa (SIGRID)",
        "url": "https://sigrid.cenepred.gob.pe/arcgis/rest/services/Peligros/Susceptibilidad_Movimiento_Masa/MapServer",
        "type": "arcgis_mapserver",
        "category": "Clima y Riesgos",
        "description": "Mapas de susceptibilidad a movimientos en masa, aludes, derrumbes e inestabilidad de laderas.",
        "crs_warning": False,
        "tags": ["deslizamientos", "laderas", "movimiento en masa", "huaicos", "cenepred", "sigrid"]
    },

    # --- COFOPRI ---
    {
        "institution": "COFOPRI",
        "name": "Catastro de Sectores Urbanos",
        "url": "https://geocat.cofopri.gob.pe/arcgis/rest/services/Catastro/Sectores_Urbanos/MapServer",
        "type": "arcgis_mapserver",
        "category": "Catastro y Propiedad",
        "description": "Polígonos catastrales urbanos y manzanas formalizadas por el Organismo de Formalización de la Propiedad Informal.",
        "crs_warning": False,
        "tags": ["manzanas", "catastro", "urbano", "predios", "cofopri"]
    },

    # --- OSINERGMIN ---
    {
        "institution": "OSINERGMIN",
        "name": "Líneas de Electricidad y Transmisión",
        "url": "https://geoportal.osinergmin.gob.pe/arcgis/rest/services/Electricidad/MapServer",
        "type": "arcgis_mapserver",
        "category": "Límites y Cartografía",
        "description": "Infraestructura del Sistema Eléctrico Interconectado Nacional (SEIN), subestaciones, líneas de alta tensión.",
        "crs_warning": False,
        "tags": ["electricidad", "sein", "subestaciones", "energia", "osinergmin"]
    },
    {
        "institution": "OSINERGMIN",
        "name": "Infraestructura de Hidrocarburos",
        "url": "https://geoportal.osinergmin.gob.pe/arcgis/rest/services/Hidrocarburos/MapServer",
        "type": "arcgis_mapserver",
        "category": "Límites y Cartografía",
        "description": "Ubicación de gasoductos (Camisea, etc.), oleoductos, plantas de almacenamiento de gas y grifos autorizados.",
        "crs_warning": False,
        "tags": ["gasoducto", "oleoducto", "gasolineras", "hidrocarburos", "osinergmin"]
    },

    # --- OEFA ---
    {
        "institution": "OEFA",
        "name": "Pasivos Ambientales de Hidrocarburos",
        "url": "https://oefa.gob.pe/arcgis/rest/services/Pasivos_Ambientales/MapServer",
        "type": "arcgis_mapserver",
        "category": "Medio Ambiente",
        "description": "Ubicación y estado de los pasivos ambientales del sector hidrocarburos evaluados por la OEFA (pozos mal sellados, derrames históricos).",
        "crs_warning": False,
        "tags": ["derrames", "pasivos", "petroleo", "contaminacion", "oefa"]
    },
    {
        "institution": "OEFA",
        "name": "Monitoreo y Calidad Ambiental",
        "url": "https://oefa.gob.pe/arcgis/rest/services/Monitoreo_Ambiental/MapServer",
        "type": "arcgis_mapserver",
        "category": "Medio Ambiente",
        "description": "Puntos de monitoreo ambiental de agua, suelo, ruido y aire a nivel nacional coordinados por OEFA.",
        "crs_warning": False,
        "tags": ["monitoreo", "calidad", "agua", "ruido", "aire", "oefa"]
    },

    # --- MINAM ---
    {
        "institution": "MINAM",
        "name": "Geoservidor Temático Nacional (WMS)",
        "url": "https://geoservidorperu.minam.gob.pe/arcgis/services/ServicioTematico/MapServer/WMSServer",
        "type": "wms",
        "category": "Medio Ambiente",
        "description": "Servicio WMS central del Geoservidor del Ministerio del Ambiente. Contiene ecosistemas, zonas degradadas, humedales, y comunidades nativas.",
        "crs_warning": False,
        "tags": ["geoservidor", "minam", "comunidades nativas", "ecosistemas", "wms"]
    },
    {
        "institution": "MINAM",
        "name": "Zonificación Ecológica Económica (ZEE)",
        "url": "https://geoservidorperu.minam.gob.pe/arcgis/rest/services/ZEE/MapServer",
        "type": "arcgis_mapserver",
        "category": "Medio Ambiente",
        "description": "Estudios departamentales y locales aprobados de Zonificación Ecológica Económica (ZEE) para el ordenamiento territorial.",
        "crs_warning": False,
        "tags": ["zee", "ordenamiento", "zonificacion", "territorio", "minam"]
    },

    # --- SUNARP ---
    {
        "institution": "SUNARP",
        "name": "Visor Catastral Registral",
        "url": "https://visor.sunarp.gob.pe/arcgis/rest/services/VisorCatastral/MapServer",
        "type": "arcgis_mapserver",
        "category": "Catastro y Propiedad",
        "description": "Límites de predios inscritos en el Registro de Predios de la SUNARP de manera referencial. Excelente para ubicar ámbitos inscritos.",
        "crs_warning": False,
        "tags": ["registral", "sunarp", "predios", "propiedad", "lotes"]
    },

    # --- MINISTERIO DE CULTURA (MINCUL) ---
    {
        "institution": "MINCUL (Cultura)",
        "name": "Patrimonio Arqueológico y Monumental",
        "url": "https://geoservicios.cultura.gob.pe/arcgis/rest/services/Patrimonio_Arqueologico/MapServer",
        "type": "arcgis_mapserver",
        "category": "Arqueología y Cultura",
        "description": "Zonas y monumentos arqueológicos prehispánicos declarados Patrimonio Cultural de la Nación. Ámbitos CIRA y reservas arqueológicas. ¡Sujeto a CRS histórico en mapas antiguos!",
        "crs_warning": True,
        "tags": ["arqueologia", "monumentos", "cira", "prehispanico", "patrimonio", "mincul"]
    },
    {
        "institution": "MINCUL (Cultura)",
        "name": "Patrimonio Arqueológico (WMS)",
        "url": "https://geoservicios.cultura.gob.pe/arcgis/services/Patrimonio_Arqueologico/MapServer/WMSServer",
        "type": "wms",
        "category": "Arqueología y Cultura",
        "description": "Conexión WMS oficial para la visualización del catastro arqueológico nacional y ámbitos CIRA de protección prehispánica.",
        "crs_warning": True,
        "tags": ["arqueologia", "monumentos", "cira", "wms", "mincul"]
    },

    # --- SUNASS ---
    {
        "institution": "SUNASS",
        "name": "Cobertura y Saneamiento",
        "url": "https://sunass.gob.pe/arcgis/rest/services/Saneamiento/MapServer",
        "type": "arcgis_mapserver",
        "category": "Hidrología y Agua",
        "description": "Áreas de prestación de servicios de saneamiento de agua potable a nivel urbano y rural en el Perú.",
        "crs_warning": False,
        "tags": ["agua potable", "saneamiento", "eps", "cobertura", "sunass"]
    },

    # --- MUNICIPALIDADES Y GOBIERNOS REGIONALES ---
    {
        "institution": "Municipalidad Metropolitana de Lima",
        "name": "Zonificación de Lima Metropolitana",
        "url": "https://imp.gob.pe/arcgis/rest/services/Zonificacion/MapServer",
        "type": "arcgis_mapserver",
        "category": "Catastro y Propiedad",
        "description": "Capas de zonificación y uso del suelo urbano oficial de Lima Metropolitana provistas por el Instituto Metropolitano de Planificación (IMP).",
        "crs_warning": False,
        "tags": ["zonificacion", "lima", "urbano", "imp", "mml"]
    },
    {
        "institution": "GORE Arequipa",
        "name": "Geoportal de Arequipa (Planificación)",
        "url": "http://geoportal.regionarequipa.gob.pe/arcgis/rest/services/Planificacion/MapServer",
        "type": "arcgis_mapserver",
        "category": "Límites y Cartografía",
        "description": "Información regional de planificación territorial, límites provinciales internos de Arequipa y proyectos locales.",
        "crs_warning": False,
        "tags": ["arequipa", "gore", "region", "planificacion"]
    },
    {
        "institution": "GORE Cajamarca",
        "name": "Geoportal de Cajamarca (Temático)",
        "url": "http://geoportal.regioncajamarca.gob.pe/arcgis/rest/services/Tematico/MapServer",
        "type": "arcgis_mapserver",
        "category": "Límites y Cartografía",
        "description": "Información regional de Cajamarca: recursos naturales, áreas de conservación regional y límites departamentales detallados.",
        "crs_warning": False,
        "tags": ["cajamarca", "gore", "region", "tematico"]
    }
]
