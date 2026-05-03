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
    
    # 1. Determinamos la visibilidad progresiva (esto lo mantenemos, es muy útil)
    todas_usuario = set(list(aprobadas) + list(regulares) + reco_cods)
    if todas_usuario:
        max_anio_actual = max([int(c[0]) for c in todas_usuario])
    else:
        max_anio_actual = 1
    limite_visibilidad = max_anio_actual + 1

    for cod, data in PLAN_ESTUDIOS.items():
        nivel = int(cod[0])
        
        if nivel <= limite_visibilidad:
            # Lógica de colores (igual que antes)
            color = "#333333" # Bloqueada
            if cod in aprobadas: color = "#2ecc71" # Verde (Aprobada)
            elif cod in regulares: color = "#3498db" # Azul (Regular)
            elif cod in reco_cods: color = "#f1c40f" # Amarillo (Sugerida)
            
            # --- AJUSTES DE DISEÑO PARA ESTILO ÁRBOL ---
            # Usamos formas geométricas simples y fuentes claras
            nodes.append(Node(
                id=cod, 
                label=f"{cod}\n{data['nombre']}", 
                size=25, # Un tamaño uniforme
                color=color,
                level=nivel, # Crucial para la jerarquía
                font={'color': 'white', 'size': 12, 'face': 'arial'},
                shape="dot" # O "circle" si prefieres
            ))
            
            deps = set(data.get("req_cursar_apr", []) + data.get("req_cursar_reg", []) + data.get("req_rendir_apr", []))
            for d in deps:
                if int(d[0]) <= limite_visibilidad:
                    # Flechas más limpias y finas para las "ramas"
                    edges.append(Edge(source=d, target=cod, color="#666666", width=1))
            
    # --- CONFIGURACIÓN DE ÁRBOL ESTÁTICO Y LIMPIO ---
    config = Config(
        width=1000, 
        height=600, 
        directed=True,
        physics=False,  # ¡IMPORTANTE! Desactivamos física para que parezca un diagrama estático
        hierarchical=True, # Activa la estructura de árbol
        direction='LR',  # De Izquierda a Derecha (estilo timeline)
        sortMethod='directed', # Mantiene el orden jerárquico
        nodeSpacing=150, # Espacio vertical entre "nodos" del mismo nivel
        levelSeparation=300, # Espacio horizontal entre niveles (Año 1 -> Año 2)
        shakeBeforeLayout=True # Ayuda a que se acomode bien al principio
    )
    
    return agraph(nodes=nodes, edges=edges, config=config)

# --- SIDEBAR (Entrada de datos) ---
# --- SIDEBAR (Con persistencia de datos) ---
with st.sidebar:
    st.header("Memoria de Trabajo")
    cuatri_actual = st.radio("Cuatrimestre a cursar:", [1, 2], horizontal=True)

    # 1. Inicializar las claves en session_state si no existen
    if "aprobadas_state" not in st.session_state:
        st.session_state.aprobadas_state = []
    if "regulares_state" not in st.session_state:
        st.session_state.regulares_state = []

    # 2. Selector de Aprobadas
    aprobadas = st.multiselect(
        "Finales Aprobados:",
        options=list(PLAN_ESTUDIOS.keys()),
        default=st.session_state.aprobadas_state,
        format_func=lambda x: f"[{x}] {PLAN_ESTUDIOS[x]['nombre']}",
        key="aprobadas_selector"
    )
    # Actualizamos el estado
    st.session_state.aprobadas_state = aprobadas

    # 3. Filtrar opciones para regulares (esto es lo que causaba el borrado)
    opciones_para_regulares = [m for m in PLAN_ESTUDIOS.keys() if m not in aprobadas]
    
    # 4. LIMPIEZA INTELIGENTE: 
    # Filtramos las regulares seleccionadas para que solo queden las que no han sido aprobadas
    regulares_limpias = [r for r in st.session_state.regulares_state if r in opciones_para_regulares]

    regulares = st.multiselect(
        "Cursadas Regulares:",
        options=opciones_para_regulares,
        default=regulares_limpias, # Aquí forzamos que mantenga las que queden
        format_func=lambda x: f"[{x}] {PLAN_ESTUDIOS[x]['nombre']}",
        key="regulares_selector"
    )
    # Actualizamos el estado
    st.session_state.regulares_state = regulares

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