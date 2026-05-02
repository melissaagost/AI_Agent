import streamlit as st
from motor_inferencia import MotorInferenciaExperto
from base_conocimiento import PLAN_ESTUDIOS

# Configuración de la página (Debe ser la primera llamada de Streamlit)
st.set_page_config(
    page_title="Experto Académico LSI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para darle un toque premium
st.markdown("""
<style>
    .metric-card {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #4CAF50;
    }
    .filtro-badge {
        background-color: #ff4b4b;
        color: white;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        font-weight: bold;
    }
    .materia-title {
        font-size: 1.2em;
        font-weight: 600;
        margin-bottom: 0px;
    }
</style>
""", unsafe_allow_html=True)

st.title("Sistema Experto de Planificación Académica")
st.markdown("### Licenciatura en Sistemas de Información (Plan 2010)")
st.markdown("---")

# 1. SECCIÓN DE ADQUISICIÓN DE CONOCIMIENTO (Entrada de Hechos)
with st.sidebar:
    st.header("Memoria de Trabajo")
    st.info("Ingresá tus datos para que el motor evalúe tu situación.")
    
    cuatri_actual = st.radio("Cuatrimestre a cursar:", [1, 2], index=0, horizontal=True)
    
    # Selector de Materias Aprobadas
    opciones_materias = list(PLAN_ESTUDIOS.keys())
    
    aprobadas = st.multiselect(
        "Materias Aprobadas:",
        options=opciones_materias,
        format_func=lambda x: f"[{x}] {PLAN_ESTUDIOS[x]['nombre']}",
        help="Seleccioná las materias que ya rendiste y aprobaste el final."
    )
    
    # Selector de Materias Regulares (excluyendo las aprobadas)
    opciones_regulares = [m for m in opciones_materias if m not in aprobadas]
    
    regulares = st.multiselect(
        "Materias Regulares:",
        options=opciones_regulares,
        format_func=lambda x: f"[{x}] {PLAN_ESTUDIOS[x]['nombre']}",
        help="Seleccioná las materias de las que tenés la regularidad (pero no el final)."
    )

# 2. EJECUCIÓN DEL MOTOR DE INFERENCIA
motor = MotorInferenciaExperto()
motor.cargar_memoria_trabajo(aprobadas, regulares, cuatri_actual)
recomendaciones = motor.ejecutar_ciclo_inferencia()

# 3. PANEL DE ESTADÍSTICAS
col1, col2, col3 = st.columns(3)
with col1:
    # 28 materias en total según el plan para el título de grado
    porcentaje_aprobadas = len(aprobadas) / 28 * 100 if len(aprobadas) <= 28 else 100
    st.metric(label="Progreso de Carrera (Aprobadas)", value=f"{len(aprobadas)}/28", delta=f"{porcentaje_aprobadas:.1f}%")
with col2:
    st.metric(label="Materias Regulares", value=len(regulares))
with col3:
    st.metric(label="Sugerencias Disponibles", value=len(recomendaciones))

st.markdown("---")

# 4. MÓDULO DE EXPLICACIÓN (Salida del Sistema Experto)
st.header(f"Recomendaciones del Experto para el {cuatri_actual}° Cuatrimestre")

if recomendaciones:
    st.success(f"El Motor de Inferencia analizó tu historial y derivó **{len(recomendaciones)}** materias habilitadas. Están ordenadas por su impacto en tu trayectoria futura (heurística de cierre transitivo).")
    
    # Mostrar resultados en tarjetas
    for i, (cod, impacto) in enumerate(recomendaciones):
        materia = PLAN_ESTUDIOS[cod]
        es_filtro = materia.get("filtro", False)
        badge = "<span class='filtro-badge'>FILTRO</span>" if es_filtro else ""
        
        with st.expander(f"#{i+1} | {materia['nombre']} (Prioridad: Alta)" if i < 3 else f"#{i+1} | {materia['nombre']}"):
            st.markdown(f"<p class='materia-title'>{materia['nombre']} {badge}</p>", unsafe_allow_html=True)
            st.caption(f"Área: {materia['area']} | Código: {cod}")
            
            st.write("**Justificación Lógica (Por qué podés cursarla):**")
            req_apr_nombres = [PLAN_ESTUDIOS[r]["nombre"] for r in materia["req_apr"]]
            req_reg_nombres = [PLAN_ESTUDIOS[r]["nombre"] for r in materia["req_reg"]]
            
            if not req_apr_nombres and not req_reg_nombres:
                st.write("- La regla no tiene precondiciones (Materia inicial sin correlativas).")
            else:
                if req_apr_nombres:
                    st.write(f"- Cumplís los requisitos aprobados: {', '.join(req_apr_nombres)}")
                if req_reg_nombres:
                    st.write(f"- Cumplís los requisitos regulares: {', '.join(req_reg_nombres)}")
            
            st.info(f"**Heurística (Por qué deberías cursarla):** Esta materia tiene un impacto transitivo de **{impacto}**. Esto significa que al aprobarla, desbloqueas directa e indirectamente el camino hacia otras {impacto} materias en el plan de estudios.")

else:
    st.warning("El motor no encontró reglas que se disparen con los hechos actuales en la Memoria de Trabajo. Verifica si te faltan cargar materias o si no hay opciones en este cuatrimestre.")