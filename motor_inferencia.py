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
        # Una materia aprobada cuenta también como regular para los requisitos
        hechos_reg_extendidos = self.mt["regulares"].union(hechos_aprobados)
        periodo = self.mt["cuatrimestre_percibido"]
        habilitadas = []

        for cod, data in self.bc.items():
            # No sugerimos materias que ya están aprobadas o regulares
            if cod not in hechos_aprobados and cod not in self.mt["regulares"]:
                # Modus Ponens: Verificación de condiciones
                cumple_apr = all(r in hechos_aprobados for r in data["req_apr"])
                cumple_reg = all(r in hechos_reg_extendidos for r in data["req_reg"])
                
                # Restricción Situada: Contexto temporal
                es_periodo_valido = (data["cuatri"] == periodo) or (data["cuatri"] == "Anual")
                
                if cumple_apr and cumple_reg and es_periodo_valido:
                    habilitadas.append(cod)
        
        return habilitadas

    def _obtener_nodos_descendientes(self, cod_materia, visitados=None):
        """
        Busca todas las materias futuras que dependen (directa o indirectamente) de la materia actual.
        """
        if visitados is None:
            visitados = set()
            
        if cod_materia in visitados:
            return set()
            
        visitados.add(cod_materia)
        descendientes = set()
        
        for cod_futura, data_futura in self.bc.items():
            if cod_materia in data_futura["req_reg"] or cod_materia in data_futura["req_apr"]:
                descendientes.add(cod_futura)
                descendientes.update(self._obtener_nodos_descendientes(cod_futura, visitados))
                
        return descendientes

    def calcular_impacto_transitivo(self, cod_materia):
        if cod_materia not in self._cache_impacto:
            nodos = self._obtener_nodos_descendientes(cod_materia)
            self._cache_impacto[cod_materia] = len(nodos)
        return self._cache_impacto[cod_materia]

    def aplicar_heuristica(self, habilitadas):
        """
        Resolución de Conflictos: Prioriza las reglas disparadas según utilidad futura.
        Utiliza el 'Cierre Transitivo' para encontrar cuellos de botella reales en la trayectoria.
        """
        # Ordenamos de mayor a menor impacto transitivo
        # Criterio secundario de desempate: Si es materia "filtro"
        return sorted(
            habilitadas, 
            key=lambda x: (
                self.calcular_impacto_transitivo(x), 
                1 if self.bc[x].get("filtro") else 0
            ), 
            reverse=True
        )

    def ejecutar_ciclo_inferencia(self):
        """
        Ciclo principal: Percibir -> Razonar -> Concluir.
        Retorna la lista de materias ordenadas y su metadata heurística.
        """
        # Fase 1: Match
        reglas_disparadas = self._evaluar_reglas()
        
        # Fase 2: Heurística
        conclusiones_ordenadas = self.aplicar_heuristica(reglas_disparadas)
        
        # Fase 3: Resultado enriquecido para el Módulo de Explicación
        resultado = []
        for cod in conclusiones_ordenadas:
            impacto = self.calcular_impacto_transitivo(cod)
            resultado.append((cod, impacto))
            
        return resultado