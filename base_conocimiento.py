
def obtener_reglas_correlatividad(codigo_materia):
    """Simula una consulta a la base de reglas."""
    materia = PLAN_ESTUDIOS.get(codigo_materia)
    return {
        "aprobadas_necesarias": materia["req_cursar_apr"],
        "regulares_necesarias": materia["req_cursar_reg"]
    }

# Contiene el conocimiento experto del dominio (Plan LSI 2010)
PLAN_ESTUDIOS = {
    # --- PRIMER AÑO ---
    "101": {"nombre": "Algoritmos y Estructuras de Datos I", "req_cursar_reg": [], "req_cursar_apr": [], "area": "Programación", "filtro": False, "cuatri": 1},
    "102": {"nombre": "Álgebra", "req_cursar_reg": [], "req_cursar_apr": [], "area": "Ciencias Básicas", "filtro": True, "cuatri": 1},
    "103": {"nombre": "Algoritmos y Estructuras de Datos II", "req_cursar_reg": ["101"], "req_cursar_apr": [], "req_rendir_apr":["101"], "area": "Programación", "filtro": False, "cuatri": 2},
    "104": {"nombre": "Lógica y Matemática Computacional", "req_cursar_reg": [], "req_cursar_apr": ["102"], "area": "Ciencias Comp.", "filtro": True, "cuatri": 2},
    "105": {"nombre": "Sistemas y Organizaciones", "req_cursar_reg": [], "req_cursar_apr": [], "area": "Sistemas", "filtro": False, "cuatri": 2},

    # --- SEGUNDO AÑO ---
    "201": {"nombre": "Paradigmas y Lenguajes", "req_cursar_reg": ["103"], "req_cursar_apr": ["101"], "req_rendir_apr":["103"], "area": "Programación", "filtro": False, "cuatri": 1},
    "202": {"nombre": "Arquitectura y Org. de Computadoras", "req_cursar_reg": ["104"], "req_cursar_apr": ["101"], "req_rendir_apr":["104"], "area": "Computación", "filtro": True, "cuatri": 1},
    "203": {"nombre": "Cálculo Diferencial e Integral", "req_cursar_reg": ["104"], "req_cursar_apr": ["102"], "req_rendir_apr":["102", "104"], "area": "Ciencias Básicas", "filtro": False, "cuatri": 1},
    "204": {"nombre": "Programación Orientada a Objetos", "req_cursar_reg": ["201"], "req_cursar_apr": ["103"], "req_rendir_apr":["103", "201"], "area": "Programación", "filtro": False, "cuatri": 2},
    "205": {"nombre": "Sistemas Operativos", "req_cursar_reg": ["202"], "req_cursar_apr": ["103"], "req_rendir_apr":["103", "202"], "area": "Computación", "filtro": True, "cuatri": 2},
    "206": {"nombre": "Administración y Gestión de Org.", "req_cursar_reg": ["105"], "req_cursar_apr": [], "req_rendir_apr":["105"], "area": "Sistemas", "filtro": False, "cuatri": 2},

    # --- TERCER AÑO ---
    "301": {"nombre": "Taller de Programación I", "req_cursar_reg": ["204"], "req_cursar_apr": ["201"], "req_rendir_apr":["204"], "area": "Programación", "filtro": False, "cuatri": 1},
    "302": {"nombre": "Comunicaciones de Datos", "req_cursar_reg": ["205"], "req_cursar_apr": ["202"], "req_rendir_apr":["205"],"area": "Computación", "filtro": False, "cuatri": 1},
    "303": {"nombre": "Ingeniería de Software I", "req_cursar_reg": ["204", "206"], "req_cursar_apr": ["105"], "req_rendir_apr":["204", "206"],"area": "Sistemas", "filtro": True, "cuatri": 1},
    "304": {"nombre": "Taller de Programación II", "req_cursar_reg": ["301", "303"], "req_cursar_apr": ["204", "205"], "req_rendir_apr":["301", "303"],"area": "Programación", "filtro": False, "cuatri": 2},
    "305": {"nombre": "Probabilidad y Estadística", "req_cursar_reg": ["203"], "req_cursar_apr": [], "req_rendir_apr":["203"],"area": "Ciencias Básicas", "filtro": False, "cuatri": 2},
    "306": {"nombre": "Bases de Datos I", "req_cursar_reg": ["204"], "req_cursar_apr": ["202"], "req_rendir_apr":["303"],"area": "Sistemas", "filtro": True, "cuatri": 2},
    "307": {"nombre": "Inglés Técnico Informático", "req_cursar_reg": [], "req_cursar_apr": [], "area": "Sistemas", "filtro": False, "cuatri": 2},

    # --- CUARTO AÑO ---
    "401": {"nombre": "Ingeniería de Software II", "req_cursar_reg": ["303"], "req_cursar_apr": ["206"], "req_rendir_apr":["303"],"area": "Sistemas", "filtro": False, "cuatri": 1},
    "402": {"nombre": "Economía Aplicada", "req_cursar_reg": ["303"], "req_cursar_apr": ["206"], "req_rendir_apr":["303"],"area": "Sistemas", "filtro": False, "cuatri": 1},
    "403": {"nombre": "Teoría de la Computación", "req_cursar_reg": ["305"], "req_cursar_apr": ["202"], "req_rendir_apr":["202", "305"], "area": "Ciencias Comp.", "filtro": False, "cuatri": 1},
    "404": {"nombre": "Redes de Datos", "req_cursar_reg": ["302"], "req_cursar_apr": [], "req_rendir_apr":["302"], "area": "Computación", "filtro": False, "cuatri": 2},
    "405": {"nombre": "Bases de Datos II", "req_cursar_reg": ["306"], "req_cursar_apr": ["303"], "area": "Sistemas", "filtro": False, "cuatri": 2},
    "406": {"nombre": "Métodos Computacionales", "req_cursar_reg": ["305"], "req_cursar_apr": ["203"], "req_rendir_apr":["305"], "area": "Ciencias Comp.", "filtro": False, "cuatri": 2},

    # --- QUINTO AÑO ---
    "501": {"nombre": "Proyecto Final de Carrera", "req_cursar_reg": ["404", "405"], "req_cursar_apr": ["401"], "area": "Sistemas", "filtro": True, "cuatri": "Anual"},
    "502": {"nombre": "Auditoría y Seguridad Informática", "req_cursar_reg": ["404", "405"], "req_cursar_apr": ["401"], "req_rendir_apr":["404", "405"], "area": "Sistemas", "filtro": False, "cuatri": 1},
    "503": {"nombre": "Optativa I", "req_cursar_reg": ["403"], "req_cursar_apr": ["305"], "req_rendir_apr":["403"], "area": "Ciencias Comp.", "filtro": False, "cuatri": 1},
    "504": {"nombre": "Optativa II", "req_cursar_reg": ["404"], "req_cursar_apr": ["302"], "req_rendir_apr":["404"], "area": "Computación", "filtro": False, "cuatri": 2},
    "505": {"nombre": "Optativa III", "req_cursar_reg": ["405"], "req_cursar_apr": ["401"], "req_rendir_apr":["405"],"area": "Sistemas", "filtro": False, "cuatri": 2},
}