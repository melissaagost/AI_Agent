# Sistema Experto de Planificación Académica - LSI Plan 2010

Este proyecto implementa un Sistema Experto (SE) diseñado para asistir a los estudiantes de la Licenciatura en Sistemas de Información (FaCENA-UNNE) en la gestión de sus trayectorias académicas. El sistema ha evolucionado de un agente basado en metas a una arquitectura de Sistema Basado en el Conocimiento (SBC), separando estrictamente el saber experto de los mecanismos de razonamiento e incorporando lógica avanzada de grafos.

---

## 🛠️ Arquitectura del Sistema
El sistema se divide en tres componentes fundamentales que respetan la estructura clásica de la IA Simbólica:

### 1. Base de Conocimiento (base_conocimiento.py)
Contiene el conocimiento formalizado del dominio. Representa el Plan de Estudios 2010 como un conjunto de Hechos Estáticos y Reglas de Producción (correlatividades).
- **Representación:** Cada asignatura se codifica con sus precondiciones exactas de aprobación (`req_apr`) y regularidad (`req_reg`).

### 2. Memoria de Trabajo (motor_inferencia.py)
Es el componente dinámico que almacena los Hechos Específicos del caso en estudio.
- Contiene el historial académico actual del alumno (materias **aprobadas** y **regulares**) y el cuatrimestre percibido.
- Es volátil: se actualiza en cada ciclo de consulta para procesar nuevos perfiles de estudiantes.

### 3. Motor de Inferencia (motor_inferencia.py)
Es el "cerebro" del sistema que coordina el razonamiento mediante un ciclo de Reconocimiento-Acción:
- **Estrategia de Razonamiento:** Utiliza Encadenamiento hacia Adelante (Forward Chaining). Parte de los hechos presentes en la Memoria de Trabajo para derivar nuevas conclusiones (materias habilitadas).
- **Modus Ponens:** Aplica lógica formal para disparar reglas cuando las precondiciones (hechos) coinciden con la Base de Conocimiento. Sabe distinguir lógicamente que una materia regular habilita el cursado, pero no un requisito de aprobación.
- **Resolución de Conflictos (Heurística Avanzada por Cierre Transitivo):** Cuando múltiples reglas se disparan simultáneamente, el motor aplica un algoritmo de búsqueda en grafos (DFS) para calcular el **Impacto Transitivo** de cada materia. No solo evalúa cuántas materias desbloquea inmediatamente, sino cuántas materias desbloquea en cascada hasta el final de la carrera. Esto imita la intuición de un tutor humano al detectar los verdaderos "cuellos de botella" del plan de estudios.

---

## 🖥️ Interfaz y Módulo de Explicación
La interfaz (`interfaz_experta.py`) actúa como el canal de Adquisición de Conocimientos y salida de resultados.
- **Diseño Premium:** Utiliza componentes visuales avanzados de Streamlit para una experiencia de usuario inmersiva y clara.
- **Módulo de Explicación:** A diferencia de un software convencional ("caja negra"), este SE justifica sus decisiones. El sistema explica qué reglas se activaron, por qué se cumplen los requisitos y expone su razonamiento heurístico (el impacto transitivo calculado), cumpliendo con el requisito fundamental de "explicabilidad" de la Inteligencia Artificial.

---

## 🚀 Conceptos de IA Aplicados
- **Agente Situado:** El sistema percibe el contexto (cuatrimestre actual, estado académico) a través de sensores en la interfaz.
- **Cierre Transitivo (Teoría de Grafos):** Evaluación recursiva de árboles de dependencia para optimizar la toma de decisiones.
- **Racionalidad:** El motor busca maximizar la medida de rendimiento (graduación en menor tiempo) seleccionando la acción que genera mayor utilidad futura (heurística).
- **Paradigma Simbólico:** El conocimiento es explícito, estructurado y manipulable mediante reglas lógicas clásicas.