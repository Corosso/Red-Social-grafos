import streamlit as st
from models.graph import SocialGraph
from utils.config import INTERESES_OPCIONES

def init_session_state():
    if 'perfiles' not in st.session_state:
        st.session_state['perfiles'] = {}
    if 'colaboraciones' not in st.session_state:
        st.session_state['colaboraciones'] = []
    if 'graph' not in st.session_state:
        st.session_state['graph'] = SocialGraph()

def main():
    st.set_page_config(layout="wide")
    init_session_state()
    
    perfiles = st.session_state['perfiles']
    colaboraciones = st.session_state['colaboraciones']
    graph = st.session_state['graph']
    
    st.title("Red Social Académica")
    
    col1, col2 = st.columns([2, 3])

    with col1:
        st.header("Agregar Perfil")
        tipo_usuario = st.selectbox("Tipo de usuario", ["Estudiante", "Profesor"])
        nombre = st.text_input("Nombre")
        
        if tipo_usuario == "Estudiante":
            carrera = st.text_input("Carrera")
        else:
            carrera = "Docente"
        
        intereses_seleccionados = st.multiselect("Intereses", INTERESES_OPCIONES)
        
        if "Etc." in intereses_seleccionados:
            interes_etc = st.text_input("Especifique el interés")
            if interes_etc:
                intereses_seleccionados.remove("Etc.")
                intereses_seleccionados.append(interes_etc)
        
        if st.button("Agregar/Actualizar Nodo"):
            perfiles[nombre] = {
                "carrera": carrera,
                "tipo": tipo_usuario,
                "intereses": intereses_seleccionados
            }
            graph.add_node(nombre, perfiles[nombre])
            st.success(f"Perfil de {nombre} agregado o actualizado.")
        
        st.header("Gestionar Colaboraciones")
        nodo1 = st.selectbox("Nodo 1", list(perfiles.keys()), index=None)
        nodo2 = st.selectbox("Nodo 2", list(perfiles.keys()), index=None)
        
        if st.button("Agregar Colaboración") and nodo1 and nodo2 and nodo1 != nodo2:
            colaboraciones.append((nodo1, nodo2))
            graph.add_edge(nodo1, nodo2)
            st.success(f"Colaboración entre {nodo1} y {nodo2} agregada.")
        
        if st.button("Eliminar Colaboración") and nodo1 and nodo2:
            if (nodo1, nodo2) in colaboraciones:
                colaboraciones.remove((nodo1, nodo2))
                graph.remove_edge(nodo1, nodo2)
                st.success(f"Colaboración entre {nodo1} y {nodo2} eliminada.")
        
        st.header("Buscar Intereses Comunes")
        interes_buscar = st.selectbox("Seleccione un interés para buscar perfiles relacionados", 
                                     [i for i in INTERESES_OPCIONES if i != "Etc."])
        
        if st.button("Buscar"):
            G_filtrado = graph.get_filtered_graph(interes_buscar, perfiles, colaboraciones)
            fig_filtrado = SocialGraph().draw_graph(G_filtrado)
            st.pyplot(fig_filtrado)
        
        if st.button("Restablecer Búsqueda"):
            fig_restablecido = graph.draw_graph()
            st.pyplot(fig_restablecido)

    with col2:
        st.header("Red de Colaboración")
        fig = graph.draw_graph()
        st.pyplot(fig)

    # Guardar los perfiles y colaboraciones en el estado de la sesión
    st.session_state['perfiles'] = perfiles
    st.session_state['colaboraciones'] = colaboraciones
    st.session_state['graph'] = graph

if __name__ == "__main__":
    main()