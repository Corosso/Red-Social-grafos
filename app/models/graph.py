import networkx as nx
import matplotlib.pyplot as plt
import community as community_louvain
from collections import Counter
import streamlit as st

class SocialGraph:
    
    def __init__(self):
        self.G = nx.Graph()
        
    def add_node(self, nombre, datos):
        self.G.add_node(nombre, tipo=datos["tipo"])
        
    def add_edge(self, nodo1, nodo2, peso=1):
        self.G.add_edge(nodo1, nodo2, weight=peso)
        
    def remove_edge(self, nodo1, nodo2):
        self.G.remove_edge(nodo1, nodo2)
        
    def get_filtered_graph(self, interes, perfiles, colaboraciones):
        resultados = {nombre for nombre, datos in perfiles.items() if interes in datos["intereses"]}
        G_filtrado = nx.Graph()
        for nombre in resultados:
            G_filtrado.add_node(nombre, tipo=perfiles[nombre]["tipo"])
        for colaboracion in colaboraciones:
            if len(colaboracion) == 3:
                n1, n2, peso = colaboracion
            else:
                n1, n2 = colaboracion
                peso = 1  # Valor por defecto
            if n1 in resultados and n2 in resultados:
                G_filtrado.add_edge(n1, n2, weight=peso)
        return G_filtrado
    
    def buscar_y_filtrar(self, interes):
        perfiles = st.session_state['perfiles']
        colaboraciones = st.session_state['colaboraciones']
        G_filtrado = self.get_filtered_graph(interes, perfiles, colaboraciones)
        if len(G_filtrado.nodes) == 0:
            print(f"No se encontraron nodos con el interés: {interes}")
            return None
        fig_filtrado = self.draw_graph(G=G_filtrado, fig_size=(6, 4), node_size=300, communities=True)
        return fig_filtrado

    def detect_communities(self):
        partition = community_louvain.best_partition(self.G)
        comunidades = {}

        # Agrupar nodos por comunidad detectada
        for nodo, comunidad_id in partition.items():
            if comunidad_id not in comunidades:
                comunidades[comunidad_id] = []
            comunidades[comunidad_id].append(nodo)

        nombres_generales = [
            "Comunidad de Estudio", "Comunidad de Investigación", "Comunidad de Tesis", 
            "Comunidad de Proyectos", "Comunidad de Redes", "Comunidad Académica"
        ]

        comunidades_nombradas = {}
        comunidad_mapping = {}

        interes_seleccionado = st.session_state.get('interes_seleccionado', "").strip().lower()
        comunidad_asignada = False  

        for idx, (comunidad_id, nodos) in enumerate(comunidades.items()):
            intereses_comunidad = []

            # Extraer intereses de los nodos en la comunidad
            for nodo in nodos:
                if "intereses" in self.G.nodes[nodo]:
                    intereses_comunidad.extend(self.G.nodes[nodo]["intereses"])  # Agrega los intereses del nodo

            # Determinar el nombre de la comunidad basado en el interés más común o el seleccionado
            if not comunidad_asignada and interes_seleccionado and interes_seleccionado in (i.lower() for i in intereses_comunidad):
                nombre_comunidad = f"Comunidad de {interes_seleccionado.capitalize()}"
                comunidad_asignada = True  
            elif intereses_comunidad:
                nombre_comunidad = f"Comunidad de {Counter(intereses_comunidad).most_common(1)[0][0]}"  # Interés más común
            else:
                nombre_comunidad = nombres_generales[idx % len(nombres_generales)]  # Nombre predefinido si no hay intereses

            comunidades_nombradas[nombre_comunidad] = nodos
            comunidad_mapping[comunidad_id] = nombre_comunidad

            # 🔹 Se asigna la comunidad a cada nodo en el grafo para que draw_graph() pueda usar esta info
            for nodo in nodos:
                self.G.nodes[nodo]["comunidad"] = nombre_comunidad  

            # Debug: Mostrar en consola los intereses analizados
            print(f"Comunidad '{nombre_comunidad}' tiene los intereses: {intereses_comunidad}")

        return comunidades_nombradas, comunidad_mapping

    def draw_graph(self, G=None, fig_size=(7, 4), node_size=320, communities=False, comunidad_mapping=None):
        if G is None:
            G = self.G

        pos = nx.spring_layout(self.G)
        fig, ax = plt.subplots(figsize=fig_size)

        if communities:
            partition = community_louvain.best_partition(self.G)
            community_names, comunidad_mapping = self.detect_communities()

            comunidad_colors = {comunidad_id: i for i, comunidad_id in enumerate(set(partition.values()))}
            color_map = [plt.cm.Set3(comunidad_colors[partition[n]]) for n in self.G.nodes]

            unique_communities = set(comunidad_mapping.values())

            # 🔹 Modificación: Crear un diccionario de colores basado en comunidad_mapping
            color_dict = {comunidad: plt.cm.Set3(i) for i, comunidad in enumerate(unique_communities)}

            # 🔹 Modificación: Asignar colores a los nodos según la comunidad almacenada en self.G.nodes
            color_map = [color_dict[self.G.nodes[n]["comunidad"]] if "comunidad" in self.G.nodes[n] else "gray" for n in self.G.nodes]

            handles = [
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_dict[comunidad], markersize=10) 
                for comunidad in unique_communities
            ]
            
            ax.legend(handles, unique_communities, title="Comunidades", fontsize="small", frameon=False)
        else:
            color_map = ["blue" if self.G.nodes[n]["tipo"] == "Estudiante" else "red" for n in self.G.nodes]

        nx.draw(self.G, pos, with_labels=True, node_color=color_map, ax=ax, node_size=node_size, cmap=plt.cm.Set3)
        return fig