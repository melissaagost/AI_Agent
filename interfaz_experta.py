# interfaz.py
import streamlit as st
from motor_inferencia import MotorInferenciaExperto
from base_conocimiento import PLAN_ESTUDIOS
from streamlit_agraph import agraph, Node, Edge, Config

st.set_page_config(page_title="Experto Académico LSI", layout="wide")

# --- FUNCIONES DE APOYO PARA EL GRAFO ---
def mostrar_grafo(aprobadas, regulares, recomendadas):
    nodes = []
    edges = []
    reco_cods = [r[0] for r in recomendadas]
    
    for cod, data in PLAN_ESTUDIOS.items():
        # Color del nodo
        color = "#333333" # Bloqueada
        if cod in aprobadas: color = "#2ecc71" # Verde
        elif cod in regulares: color = "#3498db" # Azul
        elif cod in reco_cods: color = "#f1c40f" # Amarillo
        
        nodes.append(Node(id=cod, label=f"{cod}\n{data['nombre']}", size=15, color=color))
        
        # Enlaces
        deps = set(data.get("req_cursar_apr", []) + data.get("req_cursar_reg", []) + data.get("req_rendir_apr", []))
        for d in deps:
            edges.append(Edge(source=d, target=cod))
            
    config = Config(width=800, height=500, directed=True, physics=False, hierarchical=True, direction='LR')
    return agraph(nodes=nodes, edges=edges, config=config)

# --- SIDEBAR (Entrada de datos) ---
with st.sidebar:
    st.header("Memoria de Trabajo")
    cuatri_actual = st.radio("Cuatrimestre a cursar:", [1, 2], horizontal=True)
    aprobadas = st.multiselect("Finales Aprobados:", options=list(PLAN_ESTUDIOS.keys()), 
                               format_func=lambda x: f"[{x}] {PLAN_ESTUDIOS[x]['nombre']}")
    opciones_reg = [m for m in PLAN_ESTUDIOS.keys() if m not in aprobadas]
    regulares = st.multiselect("Cursadas Regulares:", options=opciones_reg, 
                               format_func=lambda x: f"[{x}] {PLAN_ESTUDIOS[x]['nombre']}")

# --- LÓGICA DEL MOTOR ---
motor = MotorInferenciaExperto()
motor.cargar_memoria_trabajo(aprobadas, regulares, cuatri_actual)
recomendaciones = motor.ejecutar_ciclo_inferencia()

# --- INTERFAZ PRINCIPAL ---
st.title("Sistema Experto de Planificación Académica")

col1, col2, col3 = st.columns(3)
col1.metric("Aprobadas", f"{len(aprobadas)}/28")
col2.metric("Regulares", len(regulares))
col3.metric("Disponibles", len(recomendaciones))

tab_lista, tab_grafo = st.tabs(["📋 Recomendaciones", "🕸️ Mapa de Carrera"])

with tab_lista:
    if recomendadas := recomendaciones:
        for i, (cod, impacto) in enumerate(recomendadas):
            materia = PLAN_ESTUDIOS[cod]
            
            # LÓGICA DE ADVERTENCIA DE FINALES
            req_finales = materia.get("req_rendir_apr", [])
            faltantes = [r for r in req_finales if r not in aprobadas]
            
            with st.expander(f"#{i+1} | {materia['nombre']} (Impacto: {impacto})", key=f"exp_{cod}"):
                st.write(f"**Área:** {materia['area']}")
                
                if not faltantes:
                    st.success("✅ Estás listo para cursar y rendir.")
                else:
                    nombres_faltantes = [f"**{PLAN_ESTUDIOS[f]['nombre']}**" for f in faltantes]
                    st.warning(f"⚠️ **Atención:** Podés cursarla, pero para el final debés aprobar primero: {', '.join(nombres_faltantes)}")
                
                # Explicación de requisitos de cursado
                req_c_reg = [PLAN_ESTUDIOS[r]["nombre"] for r in materia.get("req_cursar_reg", [])]
                req_c_apr = [PLAN_ESTUDIOS[r]["nombre"] for r in materia.get("req_cursar_apr", [])]
                
                st.markdown("**Justificación de cursado:**")
                if req_c_reg: st.write(f"- Tenés regular: {', '.join(req_c_reg)}")
                if req_c_apr: st.write(f"- Tenés aprobado: {', '.join(req_c_apr)}")
                
                st.info(f"💡 Esta materia te abre paso a {impacto} materias futuras.")
    else:
        st.error("No hay materias habilitadas para este cuatrimestre.")

with tab_grafo:
    st.subheader("Visualización Jerárquica del Plan")
    st.caption("🟢 Aprobada | 🔵 Regular | 🟡 Recomendada | ⚫ Bloqueada")
    mostrar_grafo(aprobadas, regulares, recomendaciones)