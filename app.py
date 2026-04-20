import streamlit as st
from agente import AgenteAcademico
from datos_plan import PLAN_ESTUDIOS

# Configuración técnica de la página
st.set_page_config(page_title="Sistema de Soporte a Decisiones Académicas - LSI", layout="wide")

st.title("Sistema Facilitador Académico - Plan LSI 2010")
st.markdown("---")

# SECCIÓN DE SENSORES
st.sidebar.header("Parámetros del Entorno")

# Nuevo sensor: Percepción del tiempo académico
cuatri_opcion = st.sidebar.radio(
    "Seleccione el cuatrimestre que va a cursar:",
    options=[1, 2],
    format_func=lambda x: f"{x}° Cuatrimestre"
)

st.sidebar.markdown("---")

st.sidebar.header("Perfil del Estudiante")
seleccionadas = st.sidebar.multiselect(
    "Materias aprobadas (Final):",
    options=list(PLAN_ESTUDIOS.keys()),
    format_func=lambda x: f"[{x}] {PLAN_ESTUDIOS[x]['nombre']}"
)

# PROCESAMIENTO
# El agente recibe la percepción del cuatrimestre y las aprobadas
agente = AgenteAcademico(aprobadas=seleccionadas, cuatrimestre_actual=cuatri_opcion)
habilitadas = agente.motor_inferencia()
recomendadas = agente.heuristica_prioridad(habilitadas)

# SECCIÓN DE ACTUADORES
st.header(f"Inscripción Sugerida para el {cuatri_opcion}° Cuatrimestre")

if recomendadas:
    for i, cod in enumerate(recomendadas):
        materia = PLAN_ESTUDIOS[cod]
        with st.container():
            # Muestra si es anual o cuatrimestral
            tipo_cursado = "Anual" if materia['cuatri'] == "Anual" else f"{materia['cuatri']}° Cuatrimestre"
            
            st.markdown(f"### {i+1}. {materia['nombre']} (Código: {cod})")
            st.text(f"Área: {materia['area']} | Régimen: {tipo_cursado}")
            
            if materia['filtro']:
                st.error("Asignatura Crítica: Se recomienda un seguimiento intensivo.")
            
            if i == 0:
                st.success("Recomendación Estratégica: Máximo impacto en la trayectoria académica futura.")
            st.markdown("---")
else:
    st.warning(f"No hay asignaturas disponibles para cursar en el {cuatri_opcion}° Cuatrimestre con su perfil actual.")