from base_conocimiento import PLAN_ESTUDIOS

class MotorInferenciaExperto:
    """
    Representa el componente de razonamiento del Sistema Experto.
    Coordina la Memoria de Trabajo, la Base de Conocimientos y la Heurística.
    """
    def __init__(self):
        # 1. BASE DE CONOCIMIENTOS: Reglas estáticas del Plan 2010
        self.bc = PLAN_ESTUDIOS
        
        # 2. MEMORIA DE TRABAJO: Hechos dinámicos del alumno actual
        self.mt = {
            "aprobadas": set(),
            "regulares": set(),
            "cuatrimestre_percibido": None
        }

        # Caché para la heurística
        self._cache_impacto = {}

    def cargar_memoria_trabajo(self, aprobadas, regulares, cuatrimestre):
        """
        Fase de Adquisición: Carga los hechos percibidos en la MT.
        """
        self.mt["aprobadas"] = set(aprobadas)
        self.mt["regulares"] = set(regulares)
        self.mt["cuatrimestre_percibido"] = cuatrimestre

    def _evaluar_reglas(self):
        """
        Proceso de Match: Busca qué reglas de la BC se disparan con la MT actual.
        Implementa razonamiento de Encadenamiento hacia Adelante.
        """
        hechos_aprobados = self.mt["aprobadas"]
        hechos_reg_extendidos = self.mt["regulares"].union(hechos_aprobados)
        periodo = self.mt["cuatrimestre_percibido"]
        habilitadas = []

        for cod, data in self.bc.items():
            if cod not in hechos_aprobados and cod not in self.mt["regulares"]:
                # Lógica de Cursado: ¿Puedo sentarme a ver la clase?
                # Usamos los nuevos campos que definimos arriba
                cumple_apr = all(r in hechos_aprobados for r in data.get("req_cursar_apr", []))
                cumple_reg = all(r in hechos_reg_extendidos for r in data.get("req_cursar_reg", []))
                
                es_periodo_valido = (data["cuatri"] == periodo) or (data["cuatri"] == "Anual")
                
                if cumple_apr and cumple_reg and es_periodo_valido:
                    habilitadas.append(cod)
        
        return habilitadas

    def _obtener_nodos_descendientes(self, cod_materia, visitados=None):
        """
        Busca todas las materias futuras que dependen (directa o indirectamente) de la materia actual.
        """
        if visitados is None: visitados = set()
        if cod_materia in visitados: return set()
        visitados.add(cod_materia)
        descendientes = set()
        
        for cod_futura, data_f in self.bc.items():
            # Buscamos en todas las posibles dependencias
            todas_deps = set(data_f.get("req_cursar_apr", []) + 
                            data_f.get("req_cursar_reg", []) + 
                            data_f.get("req_rendir_apr", []))
            if cod_materia in todas_deps:
                descendientes.add(cod_futura)
                descendientes.update(self._obtener_nodos_descendientes(cod_futura, visitados))
        return descendientes

    def calcular_impacto_transitivo(self, cod_materia):
        if cod_materia not in self._cache_impacto:
            nodos = self._obtener_nodos_descendientes(cod_materia)
            self._cache_impacto[cod_materia] = len(nodos)
        return self._cache_impacto[cod_materia]

    def ejecutar_ciclo_inferencia(self):
        reglas_disparadas = self._evaluar_reglas()
        conclusiones = sorted(reglas_disparadas, 
                        key=lambda x: (self.calcular_impacto_transitivo(x), 
                        1 if self.bc[x].get("filtro") else 0), 
                        reverse=True)
        return [(cod, self.calcular_impacto_transitivo(cod)) for cod in conclusiones]