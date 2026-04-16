from datos_plan import PLAN_ESTUDIOS

class AgenteAcademico:
    def __init__(self, aprobadas):
        self.aprobadas = set(aprobadas)
        self.plan = PLAN_ESTUDIOS

    def motor_inferencia(self):
        """Módulo que aplica las reglas del Plan 2010 (Forward Chaining)"""
        habilitadas = []
        for cod, data in self.plan.items():
            if cod not in self.aprobadas:
                # El agente evalúa si cumple las precondiciones del entorno
                cumple_apr = all(r in self.aprobadas for r in data["req_apr"])
                # Simplificamos reg_reg como aprobadas para este prototipo acotado
                cumple_reg = all(r in self.aprobadas for r in data["req_reg"])
                
                if cumple_apr and cumple_reg:
                    habilitadas.append(cod)
        return habilitadas

    def heuristica_prioridad(self, habilitadas):
        """Analiza qué materia 'destraba' más futuro (Camino Crítico)"""
        puntuacion = {}
        for cod_h in habilitadas:
            destraba = 0
            for cod, data in self.plan.items():
                if cod_h in data["req_reg"] or cod_h in data["req_apr"]:
                    destraba += 1
            puntuacion[cod_h] = destraba
        
        # Ordenamos por las que más destraban
        return sorted(habilitadas, key=lambda x: puntuacion[x], reverse=True)