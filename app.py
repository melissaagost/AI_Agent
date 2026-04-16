import streamlit as st
from agente import AgenteAcademico
from datos_plan import PLAN_ESTUDIOS

st.set_page_config(page_title="Agente Guía LSI", page_icon="🎓")
st.title("🎓 Asistente Académico Inteligente - LSI")

# INTERFAZ DE SENSORES (Input del entorno)
st.sidebar.header("Historial del Alumno")
seleccionadas = st.sidebar.multiselect(
    "Seleccioná tus materias APROBADAS:",
    options=list(PLAN_ESTUDIOS.keys()),
    format_func=lambda x: f"{x} - {PLAN_ESTUDIOS[x]['nombre']}"
)

# PROCESAMIENTO DEL AGENTE (Cerebro)
agente = AgenteAcademico(aprobadas=seleccionadas)
habilitadas = agente.motor_inferencia()
recomendadas = agente.heuristica_prioridad(habilitadas)

# MOSTRAR RESULTADOS (Actuadores)
st.subheader("📋 Plan de Acción Sugerido")

if recomendadas:
    for i, cod in enumerate(recomendadas):
        nombre = PLAN_ESTUDIOS[cod]['nombre']
        es_filtro = PLAN_ESTUDIOS[cod]['filtro']
        
        with st.expander(f"{'🔥 ' if es_filtro else ''} {i+1}. {nombre} ({cod})"):
            if es_filtro:
                st.warning("⚠️ Esta es una materia crítica/filtro. El agente recomienda priorizar horas de estudio.")
            st.write(f"Área: {PLAN_ESTUDIOS[cod]['area']}")
            if i == 0:
                st.success("⭐ Recomendación principal: Esta materia desbloquea la mayor cantidad de opciones futuras.")
else:
    st.info("No hay nuevas materias habilitadas. ¡Seguí metiéndole a las actuales!")