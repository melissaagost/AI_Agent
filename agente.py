from datos_plan import PLAN_ESTUDIOS

class AgenteAcademico:
    """
    Clase que representa un Agente Basado en Metas.
    Utiliza un motor de inferencia de encadenamiento hacia adelante 
    para determinar el estado futuro del alumno.
    """
    def __init__(self, aprobadas, cuatrimestre_actual):
        self.aprobadas = set(aprobadas)
        self.cuatri_actual = cuatrimestre_actual
        self.plan = PLAN_ESTUDIOS

    def motor_inferencia(self):
        """
        Analiza las precondiciones de las materias y filtra por la 
        restricción temporal del cuatrimestre actual.
        """
        habilitadas = []
        for cod, data in self.plan.items():
            if cod not in self.aprobadas:
                # REGLA 1: Verificar correlatividades
                cumple_apr = all(r in self.aprobadas for r in data["req_apr"])
                cumple_reg = all(r in self.aprobadas for r in data["req_reg"])
                
                # REGLA 2: Restricción de Cuatrimestre (Entorno Situado)
                # Una materia se puede cursar si es del cuatrimestre actual o es anual
                es_periodo_valido = (data["cuatri"] == self.cuatri_actual) or (data["cuatri"] == "Anual")
                
                if cumple_apr and cumple_reg and es_periodo_valido:
                    habilitadas.append(cod)
        return habilitadas

    def heuristica_prioridad(self, habilitadas):
        """Camino crítico: Prioriza materias con mayor grado de dependencia futura."""
        puntuacion = {}
        for cod_h in habilitadas:
            destraba = 0
            for cod, data in self.plan.items():
                if cod_h in data["req_reg"] or cod_h in data["req_apr"]:
                    destraba += 1
            puntuacion[cod_h] = destraba
        return sorted(habilitadas, key=lambda x: puntuacion[x], reverse=True)