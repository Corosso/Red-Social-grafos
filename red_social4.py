import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Inicializar el estado de la sesión para perfiles y colaboraciones
if 'perfiles' not in st.session_state:
    st.session_state['perfiles'] = {}

if 'colaboraciones' not in st.session_state:
    st.session_state['colaboraciones'] = []

perfiles = st.session_state['perfiles']
colaboraciones = st.session_state['colaboraciones']

st.set_page_config(layout="wide")  # Asegurar que el contenido se distribuya bien

st.title("Red Social Académica")

col1, col2 = st.columns([2, 3])  # División de la interfaz, dejando más espacio para el grafo

with col1:
    st.header("Agregar Perfil")
    tipo_usuario = st.selectbox("Tipo de usuario", ["Estudiante", "Profesor"])
    nombre = st.text_input("Nombre")
    
    if tipo_usuario == "Estudiante":
        carrera = st.text_input("Carrera")
    else:
        carrera = "Docente"
    
    intereses_opciones = ["Proyectos Conjuntos", "Tutorías", "Publicaciones", "Etc."]
    intereses_seleccionados = st.multiselect("Intereses", intereses_opciones)
    
    if "Etc." in intereses_seleccionados:
        interes_etc = st.text_input("Especifique el interés")
        if interes_etc:
            intereses_seleccionados.remove("Etc.")
            intereses_seleccionados.append(interes_etc)
    
    if st.button("Agregar/Actualizar Nodo"):
        perfiles[nombre] = {"carrera": carrera, "tipo": tipo_usuario, "intereses": intereses_seleccionados}
        st.success(f"Perfil de {nombre} agregado o actualizado.")
    
    st.header("Gestionar Colaboraciones")
    nodo1 = st.selectbox("Nodo 1", list(perfiles.keys()), index=None)
    nodo2 = st.selectbox("Nodo 2", list(perfiles.keys()), index=None)
    
    if st.button("Agregar Colaboración") and nodo1 and nodo2 and nodo1 != nodo2:
        colaboraciones.append((nodo1, nodo2))
        st.success(f"Colaboración entre {nodo1} y {nodo2} agregada.")
    
    if st.button("Eliminar Colaboración") and (nodo1, nodo2) in colaboraciones:
        colaboraciones.remove((nodo1, nodo2))
        st.success(f"Colaboración entre {nodo1} y {nodo2} eliminada.")
    
    st.header("Buscar Intereses Comunes")
    interes_buscar = st.selectbox("Seleccione un interés para buscar perfiles relacionados", intereses_opciones[:-1])
    if st.button("Buscar"):
        resultados = [nombre for nombre, datos in perfiles.items() if interes_buscar in datos["intereses"]]
        colaboraciones_filtradas = [(n1, n2) for n1, n2 in colaboraciones if n1 in resultados or n2 in resultados]
        G_filtrado = nx.Graph()
        
        # Añadir nodos al grafo filtrado
        for nombre in resultados:
            datos = perfiles[nombre]
            G_filtrado.add_node(nombre, tipo=datos["tipo"])
        
        # Añadir aristas al grafo filtrado
        G_filtrado.add_edges_from(colaboraciones_filtradas)
        
        # Posicionar nodos en el grafo filtrado
        pos_filtrado = nx.spring_layout(G_filtrado)
        
        # Dibujar el grafo filtrado
        fig_filtrado, ax_filtrado = plt.subplots()
        color_map_filtrado = ["blue" if G_filtrado.nodes[n]["tipo"] == "Estudiante" else "red" for n in G_filtrado.nodes]
        nx.draw(G_filtrado, pos_filtrado, with_labels=True, node_color=color_map_filtrado, ax=ax_filtrado, node_size=2000)
        st.pyplot(fig_filtrado)
    
    if st.button("Restablecer Búsqueda"):
        G_restablecido = nx.Graph()
        
        # Añadir nodos al grafo restablecido
        for nombre, datos in perfiles.items():
            G_restablecido.add_node(nombre, tipo=datos["tipo"])
        
        # Añadir aristas al grafo restablecido
        G_restablecido.add_edges_from(colaboraciones)
        
        # Posicionar nodos en el grafo restablecido
        pos_restablecido = nx.spring_layout(G_restablecido)
        
        # Dibujar el grafo restablecido
        fig_restablecido, ax_restablecido = plt.subplots()
        color_map_restablecido = ["blue" if G_restablecido.nodes[n]["tipo"] == "Estudiante" else "red" for n in G_restablecido.nodes]
        nx.draw(G_restablecido, pos_restablecido, with_labels=True, node_color=color_map_restablecido, ax=ax_restablecido, node_size=2000)
        st.pyplot(fig_restablecido)

with col2:
    st.header("Red de Colaboración")
    G = nx.Graph()
    
    # Añadir nodos al grafo
    for nombre, datos in perfiles.items():
        G.add_node(nombre, tipo=datos["tipo"])
    
    # Añadir aristas al grafo
    G.add_edges_from(colaboraciones)
    
    # Posicionar nodos en el grafo
    pos = nx.spring_layout(G)
    
    # Dibujar el grafo
    fig, ax = plt.subplots()
    color_map = ["blue" if G.nodes[n]["tipo"] == "Estudiante" else "red" for n in G.nodes]
    nx.draw(G, pos, with_labels=True, node_color=color_map, ax=ax, node_size=2000)
    st.pyplot(fig)

# Guardar los perfiles y colaboraciones en el estado de la sesión
st.session_state['perfiles'] = perfiles
st.session_state['colaboraciones'] = colaboraciones