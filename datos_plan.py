PLAN_ESTUDIOS = {
    "101": {"nombre": "Algoritmos y Estructuras de Datos I", "req_reg": [], "req_apr": [], "area": "Programación", "filtro": False},
    "102": {"nombre": "Álgebra", "req_reg": [], "req_apr": [], "area": "Ciencias Básicas", "filtro": True},
    "103": {"nombre": "Algoritmos y Estructuras de Datos II", "req_reg": ["101"], "req_apr": [], "area": "Programación", "filtro": False},
    "104": {"nombre": "Lógica y Matemática Computacional", "req_reg": [], "req_apr": ["102"], "area": "Ciencias Comp.", "filtro": True},
    "105": {"nombre": "Sistemas y Organizaciones", "req_reg": [], "req_apr": [], "area": "Sistemas", "filtro": False},
    "201": {"nombre": "Paradigmas y Lenguajes", "req_reg": ["103"], "req_apr": ["101"], "area": "Programación", "filtro": False},
    "202": {"nombre": "Arquitectura y Org. de Computadoras", "req_reg": ["104"], "req_apr": ["101"], "area": "Computación", "filtro": True},
    "205": {"nombre": "Sistemas Operativos", "req_reg": ["202"], "req_apr": ["103"], "area": "Computación", "filtro": True},
}