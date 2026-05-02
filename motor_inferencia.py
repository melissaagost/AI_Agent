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
            "cuatrimestre_peribido": None
        }

    def cargar_memoria_trabajo(self, aprobadas, cuatrimestre):
        """
        Fase de Adquisición: Carga los hechos percibidos en la MT.
        """
        self.mt["aprobadas"] = set(aprobadas)
        self.mt["cuatrimestre_peribido"] = cuatrimestre

    def _evaluar_reglas(self):
        """
        Proceso de Match: Busca qué reglas de la BC se disparan con la MT actual.
        Implementa razonamiento de Encadenamiento hacia Adelante.
        """
        hechos_aprobados = self.mt["aprobadas"]
        periodo = self.mt["cuatrimestre_peribido"]
        habilitadas = []

        for cod, data in self.bc.items():
            if cod not in hechos_aprobados:
                # Modus Ponens: Verificación de condiciones de la regla
                cumple_apr = all(r in hechos_aprobados for r in data["req_apr"])
                cumple_reg = all(r in hechos_aprobados for r in data["req_reg"])
                
                # Restricción Situada: Contexto del cuatrimestre
                es_periodo_valido = (data["cuatri"] == periodo) or (data["cuatri"] == "Anual")
                
                if cumple_apr and cumple_reg and es_periodo_valido:
                    habilitadas.append(cod)
        
        return habilitadas

    def aplicar_heuristica(self, habilitadas):
        """
        Resolución de Conflictos: Prioriza las reglas disparadas según utilidad futura.
        Utiliza el concepto de 'Grado de Salida' (Camino Crítico).
        """
        puntuacion = {}
        for cod_h in habilitadas:
            # Cuenta cuántas materias futuras dependen de este hecho
            dependencias_futuras = 0
            for data in self.bc.values():
                if cod_h in data["req_reg"] or cod_h in data["req_apr"]:
                    dependencias_futuras += 1
            puntuacion[cod_h] = dependencias_futuras
        
        # Ordena de mayor a menor impacto
        return sorted(habilitadas, key=lambda x: puntuacion[x], reverse=True)

    def ejecutar_ciclo_inferencia(self):
        """
        Ciclo principal: Percibir -> Razonar (Evaluar + Heurística) -> Concluir.
        """
        # Fase 1: Encontrar todas las reglas que pueden dispararse
        reglas_disparadas = self._evaluar_reglas()
        
        # Fase 2: Ordenar la ejecución mediante la heurística de utilidad
        conclusiones_ordenadas = self.aplicar_heuristica(reglas_disparadas)
        
        return conclusiones_ordenadas