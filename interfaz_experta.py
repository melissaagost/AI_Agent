import streamlit as st
from motor_inferencia import MotorInferenciaExperto
from base_conocimiento import PLAN_ESTUDIOS

# Configuración de la página
st.set_page_config(page_title="Sistema Experto Académico - LSI", layout="wide")

st.title("🧠 Sistema Experto de Planificación Académica (Plan 2010)")
st.markdown("---")

# 1. SECCIÓN DE ADQUISICIÓN DE CONOCIMIENTO (Entrada de Hechos)
# Estos datos alimentarán la Memoria de Trabajo del sistema
st.sidebar.header("Memoria de Trabajo")
cuatri_actual = st.sidebar.radio("Cuatrimestre a cursar:", [1, 2])

seleccionadas = st.sidebar.multiselect(
    "Hechos conocidos (Materias Aprobadas):",
    options=list(PLAN_ESTUDIOS.keys()),
    format_func=lambda x: f"[{x}] {PLAN_ESTUDIOS[x]['nombre']}"
)

# 2. EJECUCIÓN DEL MOTOR DE INFERENCIA
# Paso A: Instanciar el motor (Crea la estructura con la BC)
motor = MotorInferenciaExperto()

# Paso B: Cargar la Memoria de Trabajo (Hechos dinámicos)
motor.cargar_memoria_trabajo(seleccionadas, cuatri_actual)

# Paso C: Ejecutar el ciclo de inferencia (Match + Resolución de Conflictos)
recomendadas = motor.ejecutar_ciclo_inferencia()

# 3. MÓDULO DE EXPLICACIÓN (Salida del Sistema Experto)
st.header(f"Recomendación del Experto para el {cuatri_actual}° Cuatrimestre")

if recomendadas:
    st.info("El Motor de Inferencia ha derivado las siguientes conclusiones basadas en las reglas de producción:")
    for i, cod in enumerate(recomendadas):
        materia = PLAN_ESTUDIOS[cod]
        # Característica clave de SE: Justificar la respuesta
        with st.expander(f"REGLA ACTIVADA: Sugerir {materia['nombre']} (Prioridad: {i+1})"):
            st.write(f"**Justificación Lógica:** Se han validado las precondiciones en la Base de Conocimiento.")
            st.write(f"**Hechos validados:** Correlatividades de {materia['nombre']} presentes en la Memoria de Trabajo.")
            st.info(f"**Impacto en la Trayectoria:** Esta materia desbloquea el acceso a otras asignaturas de {materia['area']}.")
else:
    st.warning("El motor no encontró reglas que se disparen con los hechos actuales en la Memoria de Trabajo.")