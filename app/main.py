import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from models.graph import SocialGraph
from utils.config import INTERESES_OPCIONES


def init_session_state():
    
    #Inicializa el estado de sesión de Streamlit.
    
    #Crea estructuras de datos para gestionar perfiles de usuarios,
    #colaboraciones entre ellos y la instancia del grafo social.
    
    if 'perfiles' not in st.session_state:
        
        #Acá creamos perfiles por defecto para que al correr el programa 
        #ya se pueda visualizar un grafo
        
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
            "intereses": ["Publicaciones"]
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
            "programa_academico": "Doctorado en Economía",
            "facultad": "Ciencias Exactas",
            "nivel": "Posgrado",
            "habilidades_tecnicas": ["Investigación", "Docencia"],
            "tipo": "Profesor",
            "intereses": ["Publicaciones"]
        },
        "Carolina Osorio": {
            "programa_academico": "Docencia",
            "facultad": "",
            "nivel": "Posgrado",
            "habilidades_tecnicas": ["Investigación", "Docencia"],
            "tipo": "Profesor",
            "intereses": ["Trabajo de investigación", "Ponencias"]
        },
        "Patricia Rincón": {
            "programa_academico": "Ingeniería en Sistemas",
            "facultad": "Ingeniería",
            "nivel": "Posgrado",
            "habilidades_tecnicas": ["Investigación", "Docencia"],
            "tipo": "Profesor",
            "intereses": ["Proyectos Conjuntos", "Tutorías"]
        },
        # 🔹 Nuevos perfiles agregados
        "Laura Gómez": {
            "programa_academico": "Ciencias Políticas",
            "facultad": "Facultad de Ciencias Sociales",
            "nivel": "Pregrado",
            "habilidades_tecnicas": ["Análisis de datos", "Política Pública"],
            "tipo": "Estudiante",
            "intereses": ["Publicaciones"]
        },
        "Felipe Torres": {
            "programa_academico": "Biología",
            "facultad": "Facultad de Ciencias Naturales",
            "nivel": "Pregrado",
            "habilidades_tecnicas": ["Genética", "Ecología"],
            "tipo": "Estudiante",
            "intereses": ["Tesis"]
        },
        "Valeria Ruiz": {
            "programa_academico": "Psicología",
            "facultad": "Facultad de Ciencias Humanas",
            "nivel": "Posgrado",
            "habilidades_tecnicas": ["Psicoterapia", "Investigación"],
            "tipo": "Profesor",
            "intereses": ["Tesis"]
        }
    }
    #Acá creamos las colaboraciones que "relacionan" los datos iniciales
    if 'colaboraciones' not in st.session_state:
        st.session_state['colaboraciones'] = [
            ("Santiago Hernández", "Patricia Rincón"),
            ("Andres Sanchez", "Lina Munera"),
            ("Cristian Llano", "Carolina Osorio"),
            ("Melisa Duran", "Patricia Rincón"),
            ("Santiago Hernández", "Lina Munera"),
            ("Andres Sanchez", "Carolina Osorio"),
            ("Cristian Llano", "Patricia Rincón"),
            ("Laura Gómez", "Santiago Hernández"),  # Relación entre estudiantes con interés en publicaciones
            ("Felipe Torres", "Andres Sanchez"),  # Relación entre estudiantes con interés en tesis
            ("Valeria Ruiz", "Cristian Llano")  # Relación entre estudiantes con interés en tesis
        ]
    if 'graph' not in st.session_state:
        st.session_state['graph'] = SocialGraph()


def main():
    
    #Configura la interfaz de usuario en Streamlit y gestiona la red social académica.
    
    st.set_page_config(layout="wide")
    #Acá vamos a realizar los estilos de la página
    st.markdown(
    """
    <style>
        /* Fondo azul marino */
        .stApp {
            background-color: #1b263b; /* Azul marino oscuro */
            color: white !important;
        }

        /* Títulos de TODOS los inputs */
        label, .stTextInput label, .stNumberInput label, .stSelectbox label, .stRadio label, .stMultiSelect label {
            font-family: 'Arial Black', sans-serif;
            color: white !important; /* Blanco para que resalten */
            text-transform: uppercase;
            font-weight: bold;
        }

        /* Inputs de texto y números */
        input[type="text"], input[type="number"], textarea {
            background-color: #415a77 !important; /* Azul más claro */
            color: white !important;
            border-radius: 5px;
            border: 2px solid #00c8ff !important; /* Borde azul claro */
        }

         /* Eliminar margen y padding de la página */
        .stApp {
            margin: 2px !important;
            padding: 2px !important;
        }

        /* Eliminar margen superior */
        header, .block-container {
            padding-top: 0,1px !important;
        }

        /* Placeholder de los inputs */
        input::placeholder, textarea::placeholder {
            color: #b0c4de !important; /* Azul claro */
        }

        /* Selectbox */
        div[data-baseweb="select"] {
            background-color: #415a77 !important;
            color: white !important;
            border: 2px solid #00c8ff !important;
            border-radius: 5px;
        }

        /* Opciones dentro del selectbox */
        div[data-baseweb="select"] * {
            color: white !important;
            background-color: #415a77 !important;
        }

        /* Botones */
        .stButton>button {
            background-color: #0077b6 !important;
            color: white !important;
            font-size: 16px;
            border-radius: 10px;
            font-weight: bold;
        }

        .stButton>button:hover {
            background-color: #005f99 !important;
        }

    </style>
    """,
    unsafe_allow_html=True
    )
    init_session_state()

    perfiles = st.session_state['perfiles']
    colaboraciones = st.session_state['colaboraciones']
    graph = st.session_state['graph']

    # Inicializar el grafo con los datos iniciales
    for nombre, datos in perfiles.items():
        graph.add_node(nombre, datos)
    for nodo1, nodo2 in colaboraciones:
        graph.add_edge(nodo1, nodo2)

    st.title("📚 Red Social Académica ✏️ ")

    col1, col2 = st.columns([2, 3])

    with col1:

         # Sección para agregar un nuevo perfil al grafo
        st.header("Agregar Perfil ➕")
         # Selección del tipo de usuario (Estudiante o Profesor)
        tipo_usuario = st.selectbox("Tipo de usuario", ["Estudiante", "Profesor"])

        #Entradas de texto para cada atributo
        nombre = st.text_input("Nombre")
        
        programa_academico = st.text_input("Programa Académico (ej. Ingeniería Civil, Medicina General)")
        
        facultad = st.text_input("Facultad")
        nivel = st.selectbox("Nivel", ["Pregrado", "Posgrado"])
        habilidades_tecnicas = st.text_area("Habilidades Técnicas (separadas por comas)", "")

        intereses_seleccionados = st.multiselect("Intereses", INTERESES_OPCIONES)
         # Si el usuario selecciona 'Etc.', se le permite especificar un nuevo interés
        if intereses_seleccionados and intereses_seleccionados[-1] == 'Etc.':
            interes_etc = st.text_input("Especifique el interés")
            if interes_etc:
                intereses_seleccionados[-1] = interes_etc

        # Botón para agregar o actualizar un nodo en el grafo
        if st.button("Agregar/Actualizar Nodo"):
            if nombre: # Verifica que el nombre no esté vacío
                perfiles[nombre] = {
                    'programa_academico': programa_academico,
                    'facultad': facultad,
                    'nivel': nivel,
                    'habilidades_tecnicas': habilidades_tecnicas.split(", "), # Convierte la cadena en una lista
                    'tipo': tipo_usuario,
                    'intereses': intereses_seleccionados
                }
                # Agregar el nodo al grafo con sus atributos
                graph.add_node(nombre, perfiles[nombre])
                st.success(f"Perfil de {nombre} agregado o actualizado.")
        
        # Sección para gestionar colaboraciones entre perfiles
        st.header("Gestionar Colaboraciones 🤝")
         # Selección de los nodos (perfiles) que colaborarán
        nodo1 = st.selectbox("Nodo 1", list(perfiles.keys()), index=None)
        nodo2 = st.selectbox("Nodo 2", list(perfiles.keys()), index=None)

        # Botón para agregar una colaboración entre dos nodos si no existe previamente
        if st.button("Agregar Colaboración") and nodo1 and nodo2 and nodo1 != nodo2:
            if (nodo1, nodo2) not in colaboraciones and (nodo2, nodo1) not in colaboraciones:
                colaboraciones.append((nodo1, nodo2)) # Agregar la relación a la lista de colaboraciones
                graph.add_edge(nodo1, nodo2) # Agregar la arista al grafo
                st.success(f"Colaboración entre {nodo1} y {nodo2} agregada.")


        # Botón para eliminar una colaboración existente entre dos nodos
        if st.button("Eliminar Colaboración") and nodo1 and nodo2:
            if (nodo1, nodo2) in colaboraciones:
                colaboraciones.remove((nodo1, nodo2)) # Eliminar de la lista de colaboraciones
                graph.remove_edge(nodo1, nodo2) # Eliminar la arista del grafo
                st.success(f"Colaboración entre {nodo1} y {nodo2} eliminada.")
            elif (nodo2, nodo1) in colaboraciones:
                colaboraciones.remove((nodo2, nodo1)) # Eliminar la relación en el otro orden
                graph.remove_edge(nodo2, nodo1)
                st.success(f"Colaboración entre {nodo2} y {nodo1} eliminada.")
            else:
                st.warning(f"No existe colaboración entre {nodo1} y {nodo2}.")
        
        # Sección para buscar perfiles con intereses comunes
        st.header("Buscar Intereses Comunes 🧩")
        # Dropdown para seleccionar un interés específico (excluyendo la opción 'Etc.')
        interes_buscar = st.selectbox("Seleccione un interés para buscar perfiles relacionados", 
                                     [i for i in INTERESES_OPCIONES if i != "Etc."])
        
        # Botón para realizar la búsqueda de perfiles relacionados con el interés seleccionado
        if st.button("Buscar"):
            fig_filtrado = graph.buscar_y_filtrar(interes_buscar)
            if fig_filtrado:
                st.pyplot(fig_filtrado)

        def buscar_y_filtrar(self, interes):
            G_filtrado = self.get_filtered_graph(interes, self.perfiles, self.colaboraciones)
            if len(G_filtrado.nodes) == 0:
                print(f"No se encontraron nodos con el interés: {interes}")
                return None
            self.draw_graph(G=G_filtrado, fig_size=(6, 4), node_size=300, communities=True)
            return G_filtrado
        
        # Botón para restablecer la búsqueda y mostrar el grafo completo
        if st.button("Restablecer Búsqueda"):
            fig_restablecido = graph.draw_graph() # Dibuja el grafo sin filtros
            st.pyplot(fig_restablecido)
        

        if st.button("Detectar Comunidades"):
            comunidades, comunidad_mapping = graph.detect_communities()  # Obtener ambas estructuras de datos

            fig_comunidades = graph.draw_graph(communities=True, comunidad_mapping=comunidad_mapping)  # Pasa comunidad_mapping
            st.pyplot(fig_comunidades)  # Muestra el grafo con las comunidades detectadas

            # Iterar sobre el diccionario de comunidades correctamente
            for comunidad, nodos in comunidades.items():
                st.write(f"La comunidad '{comunidad}' incluye los nodos: {', '.join(nodos)}")


    with col2:
        st.header("Red de Colaboración")
        # Genera la visualización del grafo con los nodos y conexiones actuales
        fig = graph.draw_graph()
        
        # Agrega una leyenda para distinguir entre estudiantes y profesores en el grafo
        fig.legend(handles=[
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Estudiantes'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Profesores')
        ], loc='upper right')
        
        st.pyplot(fig)

        # Si se ha seleccionado un primer nodo, muestra su información detallada
        if nodo1:
            datos_nodo1 = perfiles[nodo1]  # Obtiene los datos del nodo seleccionado
            st.markdown(f"### INFORMACIÓN DEL PRIMER NODO SELECCIONADO: \n\n**Nombre:** {nodo1}\n\n**Tipo:** {datos_nodo1['tipo']}\n\n**Programa Académico:** {datos_nodo1['programa_academico']}\n\n**Intereses:** {', '.join(datos_nodo1['intereses'])}")

        if nodo2:
            datos_nodo2 = perfiles[nodo2]  # Obtiene los datos del nodo seleccionado
            st.markdown(f"### INFORMACIÓN DEL SEGUNDO NODO SELECCIONADO:\n\n**Nombre:** {nodo2}\n\n**Tipo:** {datos_nodo2['tipo']}\n\n**Programa Académico:** {datos_nodo2['programa_academico']}\n\n**Intereses:** {', '.join(datos_nodo2['intereses'])}")

    st.session_state['perfiles'] = perfiles  # Almacena el diccionario de perfiles en la sesión.
    st.session_state['colaboraciones'] = colaboraciones  # Guarda la lista de colaboraciones (conexiones entre nodos).
    st.session_state['graph'] = graph  # Guarda el grafo actualizado con los nodos y relaciones.

if __name__ == "__main__":
    main()