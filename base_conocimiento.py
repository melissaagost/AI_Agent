
def obtener_reglas_correlatividad(codigo_materia):
    """Simula una consulta a la base de reglas."""
    materia = PLAN_ESTUDIOS.get(codigo_materia)
    return {
        "aprobadas_necesarias": materia["req_apr"],
        "regulares_necesarias": materia["req_reg"]
    }

# Contiene el conocimiento experto del dominio (Plan LSI 2010)
PLAN_ESTUDIOS = {
    # --- PRIMER AÑO ---
    "101": {"nombre": "Algoritmos y Estructuras de Datos I", "req_reg": [], "req_apr": [], "area": "Programación", "filtro": False, "cuatri": 1},
    "102": {"nombre": "Álgebra", "req_reg": [], "req_apr": [], "area": "Ciencias Básicas", "filtro": True, "cuatri": 1},
    "103": {"nombre": "Algoritmos y Estructuras de Datos II", "req_reg": ["101"], "req_apr": [], "area": "Programación", "filtro": False, "cuatri": 2},
    "104": {"nombre": "Lógica y Matemática Computacional", "req_reg": [], "req_apr": ["102"], "area": "Ciencias Comp.", "filtro": True, "cuatri": 2},
    "105": {"nombre": "Sistemas y Organizaciones", "req_reg": [], "req_apr": [], "area": "Sistemas", "filtro": False, "cuatri": 2},

    # --- SEGUNDO AÑO ---
    "201": {"nombre": "Paradigmas y Lenguajes", "req_reg": ["103"], "req_apr": ["101"], "area": "Programación", "filtro": False, "cuatri": 1},
    "202": {"nombre": "Arquitectura y Org. de Computadoras", "req_reg": ["104"], "req_apr": ["101"], "area": "Computación", "filtro": True, "cuatri": 1},
    "203": {"nombre": "Cálculo Diferencial e Integral", "req_reg": ["106"], "req_apr": ["102"], "area": "Ciencias Básicas", "filtro": False, "cuatri": 1},
    "204": {"nombre": "Programación Orientada a Objetos", "req_reg": ["201"], "req_apr": ["103"], "area": "Programación", "filtro": False, "cuatri": 2},
    "205": {"nombre": "Sistemas Operativos", "req_reg": ["202"], "req_apr": ["103"], "area": "Computación", "filtro": True, "cuatri": 2},
    "206": {"nombre": "Administración y Gestión de Org.", "req_reg": ["105"], "req_apr": [], "area": "Sistemas", "filtro": False, "cuatri": 2},

    # --- TERCER AÑO ---
    "301": {"nombre": "Taller de Programación I", "req_reg": ["204"], "req_apr": ["201"], "area": "Programación", "filtro": False, "cuatri": 1},
    "302": {"nombre": "Comunicaciones de Datos", "req_reg": ["205"], "req_apr": ["202"], "area": "Computación", "filtro": False, "cuatri": 1},
    "303": {"nombre": "Ingeniería de Software I", "req_reg": ["204", "206"], "req_apr": ["105"], "area": "Sistemas", "filtro": True, "cuatri": 1},
    "304": {"nombre": "Taller de Programación II", "req_reg": ["301", "303"], "req_apr": ["204", "205"], "area": "Programación", "filtro": False, "cuatri": 2},
    "305": {"nombre": "Probabilidad y Estadística", "req_reg": ["203"], "req_apr": [], "area": "Ciencias Básicas", "filtro": False, "cuatri": 2},
    "306": {"nombre": "Bases de Datos I", "req_reg": ["204"], "req_apr": ["202"], "area": "Sistemas", "filtro": True, "cuatri": 2},
    "307": {"nombre": "Inglés Técnico Informático", "req_reg": [], "req_apr": [], "area": "Sistemas", "filtro": False, "cuatri": 2},

    # --- CUARTO AÑO ---
    "401": {"nombre": "Ingeniería de Software II", "req_reg": ["303"], "req_apr": ["206"], "area": "Sistemas", "filtro": False, "cuatri": 1},
    "402": {"nombre": "Economía Aplicada", "req_reg": ["303"], "req_apr": ["206"], "area": "Sistemas", "filtro": False, "cuatri": 1},
    "403": {"nombre": "Teoría de la Computación", "req_reg": ["305"], "req_apr": ["202"], "area": "Ciencias Comp.", "filtro": False, "cuatri": 1},
    "404": {"nombre": "Redes de Datos", "req_reg": ["302"], "req_apr": [], "area": "Computación", "filtro": False, "cuatri": 2},
    "405": {"nombre": "Bases de Datos II", "req_reg": ["306"], "req_apr": ["303"], "area": "Sistemas", "filtro": False, "cuatri": 2},
    "406": {"nombre": "Métodos Computacionales", "req_reg": ["305"], "req_apr": ["203"], "area": "Ciencias Comp.", "filtro": False, "cuatri": 2},

    # --- QUINTO AÑO ---
    "501": {"nombre": "Proyecto Final de Carrera", "req_reg": ["404", "405"], "req_apr": ["401"], "area": "Sistemas", "filtro": True, "cuatri": "Anual"},
    "502": {"nombre": "Auditoría y Seguridad Informática", "req_reg": ["404", "405"], "req_apr": ["401"], "area": "Sistemas", "filtro": False, "cuatri": 1},
    "503": {"nombre": "Optativa I", "req_reg": ["403"], "req_apr": ["305"], "area": "Ciencias Comp.", "filtro": False, "cuatri": 1},
    "504": {"nombre": "Optativa II", "req_reg": ["404"], "req_apr": ["302"], "area": "Computación", "filtro": False, "cuatri": 2},
    "505": {"nombre": "Optativa III", "req_reg": ["405"], "req_apr": ["401"], "area": "Sistemas", "filtro": False, "cuatri": 2},
}