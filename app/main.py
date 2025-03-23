import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from models.graph import SocialGraph
from utils.config import INTERESES_OPCIONES

def init_session_state():
    if 'perfiles' not in st.session_state:
        st.session_state['perfiles'] = {
            "Santiago Hernández": {
                "programa_academico": "Ingeniería de Sistemas",
                "facultad": "Facultad de Ingeniería",
                "nivel": "Pregrado",
                "habilidades_tecnicas": ["Programación", "Bases de Datos"],
                "tipo": "Estudiante",
                "intereses": ["Proyectos Conjuntos", "Tutorías"]
            },
            "Andres Sanchez": {
                "programa_academico": "Medicina",
                "facultad": "Facultad de Ciencias de la Salud",
                "nivel": "Pregrado",
                "habilidades_tecnicas": ["Anatomía", "Fisiología"],
                "tipo": "Estudiante",
                "intereses": ["Publicaciones", "Tesis"]
            },
            "Cristian Llano": {
                "programa_academico": "Derecho",
                "facultad": "Facultad de Ciencias Jurídicas",
                "nivel": "Pregrado",
                "habilidades_tecnicas": ["Legislación", "Investigación Jurídica"],
                "tipo": "Estudiante",
                "intereses": ["Trabajo de investigación", "Ponencias"]
            },
            "Melisa Duran": {
                "programa_academico": "Arquitectura",
                "facultad": "Facultad de Arquitectura y Diseño",
                "nivel": "Pregrado",
                "habilidades_tecnicas": ["Diseño", "Construcción"],
                "tipo": "Estudiante",
                "intereses": ["Proyectos Conjuntos", "Tutorías"]
            },
            "Lina Munera": {
                "programa_academico": "",
                "facultad": "",
                "nivel": "",
                "habilidades_tecnicas": ["Investigación", "Docencia"],
                "tipo": "Profesor",
                "intereses": ["Publicaciones", "Tesis"]
            },
            "Carolina Osorio": {
                "programa_academico": "",
                "facultad": "",
                "nivel": "",
                "habilidades_tecnicas": ["Investigación", "Docencia"],
                "tipo": "Profesor",
                "intereses": ["Trabajo de investigación", "Ponencias"]
            },
            "Patricia Rincón": {
                "programa_academico": "",
                "facultad": "",
                "nivel": "",
                "habilidades_tecnicas": ["Investigación", "Docencia"],
                "tipo": "Profesor",
                "intereses": ["Proyectos Conjuntos", "Tutorías"]
            }
        }
    if 'colaboraciones' not in st.session_state:
        st.session_state['colaboraciones'] = [
            ("Santiago Hernández", "Patricia Rincón"),
            ("Andres Sanchez", "Lina Munera"),
            ("Cristian Llano", "Carolina Osorio"),
            ("Melisa Duran", "Patricia Rincón"),
            ("Santiago Hernández", "Lina Munera"),
            ("Andres Sanchez", "Carolina Osorio"),
            ("Cristian Llano", "Patricia Rincón")
        ]
    if 'graph' not in st.session_state:
        st.session_state['graph'] = SocialGraph()

def main():
    st.set_page_config(layout="wide")
    init_session_state()

    perfiles = st.session_state['perfiles']
    colaboraciones = st.session_state['colaboraciones']
    graph = st.session_state['graph']

    # Inicializar el grafo con los datos iniciales
    for nombre, datos in perfiles.items():
        graph.add_node(nombre, datos)
    for nodo1, nodo2 in colaboraciones:
        graph.add_edge(nodo1, nodo2)

    st.title("Red Social Académica")

    col1, col2 = st.columns([2, 3])

    with col1:
        st.header("Agregar Perfil")
        tipo_usuario = st.selectbox("Tipo de usuario", ["Estudiante", "Profesor"])
        nombre = st.text_input("Nombre")
        
        # Solo Programa Académico en lugar de Carrera
        programa_academico = st.text_input("Programa Académico (ej. Ingeniería Civil, Medicina General)")
        
        facultad = st.text_input("Facultad")
        nivel = st.selectbox("Nivel", ["Pregrado", "Posgrado"])
        habilidades_tecnicas = st.text_area("Habilidades Técnicas (separadas por comas)", "")

        # Intereses
        intereses_seleccionados = st.multiselect("Intereses", INTERESES_OPCIONES)
        
        if intereses_seleccionados and intereses_seleccionados[-1] == 'Etc.':
            interes_etc = st.text_input("Especifique el interés")
            if interes_etc:
                intereses_seleccionados[-1] = interes_etc

        if st.button("Agregar/Actualizar Nodo"):
            if nombre:  # Asegurarse de que el nombre no esté vacío
                perfiles[nombre] = {
                    'programa_academico': programa_academico,
                    'facultad': facultad,
                    'nivel': nivel,
                    'habilidades_tecnicas': habilidades_tecnicas.split(", "),
                    'tipo': tipo_usuario,
                    'intereses': intereses_seleccionados
                }
                graph.add_node(nombre, perfiles[nombre])
                st.success(f"Perfil de {nombre} agregado o actualizado.")
                
                # Restablecer los campos a su estado inicial después de agregar el perfil
                st.session_state['nombre'] = ''
                st.session_state['tipo_usuario'] = 'Estudiante'
                st.session_state['facultad'] = ''
                st.session_state['programa_academico'] = ''
                st.session_state['nivel'] = 'Pregrado'
                st.session_state['habilidades_tecnicas'] = ''
                st.session_state['intereses_seleccionados'] = []

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
            fig_filtrado = graph.draw_graph(G_filtrado)
            st.pyplot(fig_filtrado)
        
        if st.button("Restablecer Búsqueda"):
            fig_restablecido = graph.draw_graph()
            st.pyplot(fig_restablecido)
        
        # Botón para mostrar comunidades
        if st.button("Detectar Comunidades"):
            fig_comunidades = graph.draw_graph(communities=True)
            st.pyplot(fig_comunidades)

    with col2:
        st.header("Red de Colaboración")
        fig = graph.draw_graph()
        
        # Añadir leyenda
        fig.legend(handles=[
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Estudiantes'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Profesores')
        ], loc='upper right')
        
        st.pyplot(fig)

        # Mostrar información del nodo seleccionado
        if nodo1:
            datos_nodo1 = perfiles[nodo1]
            st.markdown(f"### INFORMACIÓN DEL PRIMER NODO SELECCIONADO: \n\n**Nombre:** {nodo1}\n\n**Tipo:** {datos_nodo1['tipo']}\n\n**Programa Académico:** {datos_nodo1['programa_academico']}\n\n**Intereses:** {', '.join(datos_nodo1['intereses'])}")

        if nodo2:
            datos_nodo2 = perfiles[nodo2]
            st.markdown(f"### INFORMACIÓN DEL SEGUNDO NODO SELECCIONADO:\n\n**Nombre:** {nodo2}\n\n**Tipo:** {datos_nodo2['tipo']}\n\n**Programa Académico:** {datos_nodo2['programa_academico']}\n\n**Intereses:** {', '.join(datos_nodo2['intereses'])}")

    # Guardar los perfiles y colaboraciones en el estado de la sesión
    st.session_state['perfiles'] = perfiles
    st.session_state['colaboraciones'] = colaboraciones
    st.session_state['graph'] = graph

if __name__ == "__main__":
    main()