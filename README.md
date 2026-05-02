🧠 Sistema Experto de Planificación Académica - LSI Plan 2010

Este proyecto implementa un Sistema Experto (SE) diseñado para asistir a los estudiantes de la Licenciatura en Sistemas de Información (FaCENA-UNNE) en la gestión de sus trayectorias académicas. El sistema ha evolucionado de un agente basado en metas a una arquitectura de Sistema Basado en el Conocimiento (SBC), separando estrictamente el saber experto de los mecanismos de razonamiento.


🛠️ Arquitectura del Sistema
El sistema se divide en tres componentes fundamentales que respetan la estructura clásica de la IA Simbólica:

1. Base de Conocimiento (base_conocimiento.py)
Contiene el conocimiento formalizado del dominio. Representa el Plan de Estudios 2010 como un conjunto de Hechos Estáticos y Reglas de Producción (correlatividades).

Representación: Cada asignatura se codifica con sus precondiciones de aprobación y regularidad.

2. Memoria de Trabajo (motor_inferencia.py)
Es el componente dinámico que almacena los Hechos Específicos del caso en estudio.

Contiene el historial académico actual del alumno y el cuatrimestre percibido.

Es volátil: se actualiza en cada ciclo de consulta para procesar nuevos perfiles de estudiantes.

3. Motor de Inferencia (motor_inferencia.py)
Es el "cerebro" del sistema que coordina el razonamiento mediante un ciclo de Reconocimiento-Acción:

Estrategia de Razonamiento: Utiliza Encadenamiento hacia Adelante (Forward Chaining). Parte de los hechos presentes en la Memoria de Trabajo para derivar nuevas conclusiones (materias habilitadas).

Modus Ponens: Aplica lógica formal para disparar reglas cuando las precondiciones (hechos) coinciden con la Base de Conocimiento.

Resolución de Conflictos (Heurística): Cuando múltiples reglas se disparan simultáneamente, el motor aplica una función de utilidad basada en el Camino Crítico. Prioriza aquellas asignaturas que desbloquean un mayor número de nodos (materias) en el grafo de la carrera.



🖥️ Interfaz y Módulo de Explicación
La interfaz (interfaz_experta.py) actúa como el canal de Adquisición de Conocimientos y salida de resultados.

Módulo de Explicación: A diferencia de un software convencional, este SE justifica sus decisiones. A través de una interfaz transparente, el sistema explica qué reglas se activaron y por qué (validación de hechos en la Memoria de Trabajo), cumpliendo con el requisito de explicabilidad de los Sistemas Expertos.



🚀 Conceptos de IA Aplicados
Agente Situado: El sistema percibe el "tiempo académico" a través de sensores (selector de cuatrimestre), lo que condiciona sus acciones posibles.

Racionalidad: El motor busca maximizar la medida de rendimiento (graduación óptima) seleccionando la acción que genera mayor utilidad futura.

Paradigma Simbólico: El conocimiento es explícito, estructurado y manipulable mediante reglas lógicas.