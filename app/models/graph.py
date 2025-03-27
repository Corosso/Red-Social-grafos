import networkx as nx
import matplotlib.pyplot as plt
import community as community_louvain
from collections import Counter
import streamlit as st

class SocialGraph:
    
    def __init__(self):
        # Inicializa un grafo vacío
        self.G = nx.Graph()
        
    def add_node(self, nombre, datos):
        # Agrega un nodo al grafo con un tipo asociado (ej. Estudiante o Profesor)
        self.G.add_node(nombre, tipo=datos["tipo"])
        
    def add_edge(self, nodo1, nodo2, peso=1):
        # Agrega una conexión (arista) entre dos nodos con un peso opcional
        self.G.add_edge(nodo1, nodo2, weight=peso)
        
    def remove_edge(self, nodo1, nodo2):
        # Elimina una conexión entre dos nodos
        self.G.remove_edge(nodo1, nodo2)
        
    def get_filtered_graph(self, interes, perfiles, colaboraciones):
        # Filtra el grafo basado en un interés específico
        resultados = {nombre for nombre, datos in perfiles.items() if interes in datos["intereses"]}
        G_filtrado = nx.Graph()
        
        # Agrega solo los nodos que tienen el interés buscado
        for nombre in resultados:
            G_filtrado.add_node(nombre, tipo=perfiles[nombre]["tipo"])
        
        # Agrega las conexiones (aristas) entre los nodos filtrados
        for colaboracion in colaboraciones:
            if len(colaboracion) == 3:
                n1, n2, peso = colaboracion
            else:
                n1, n2 = colaboracion
                peso = 1  # Si no se proporciona peso, se usa el valor por defecto
            if n1 in resultados and n2 in resultados:
                G_filtrado.add_edge(n1, n2, weight=peso)
        
        return G_filtrado
    
    def buscar_y_filtrar(self, interes):
        # Obtiene perfiles y colaboraciones desde Streamlit
        perfiles = st.session_state['perfiles']
        colaboraciones = st.session_state['colaboraciones']
        
        # Filtra el grafo con base en el interés proporcionado
        G_filtrado = self.get_filtered_graph(interes, perfiles, colaboraciones)
        
        if len(G_filtrado.nodes) == 0:
            print(f"No se encontraron nodos con el interés: {interes}")
            return None
        
        # Dibuja el grafo filtrado con comunidades resaltadas
        fig_filtrado = self.draw_graph(G=G_filtrado, fig_size=(6, 4), node_size=300, communities=True)
        return fig_filtrado

    def detect_communities(self):
        # Aplica el algoritmo de Louvain para detectar comunidades en el grafo
        partition = community_louvain.best_partition(self.G)
        comunidades = {}

        # Agrupa nodos en comunidades detectadas
        for nodo, comunidad_id in partition.items():
            if comunidad_id not in comunidades:
                comunidades[comunidad_id] = []
            comunidades[comunidad_id].append(nodo)
        
        # Lista de nombres genéricos para las comunidades
        nombres_generales = [
            "Comunidad de Estudio", "Comunidad de Investigación", "Comunidad de Tesis", 
            "Comunidad de Proyectos", "Comunidad de Redes", "Comunidad Académica"
        ]
        
        comunidades_nombradas = {}
        comunidad_mapping = {}
        
        # Obtiene el interés seleccionado en la UI de Streamlit
        interes_seleccionado = st.session_state.get('interes_seleccionado', "").strip().lower()
        comunidad_asignada = False  # Bandera para evitar asignar el mismo interés más de una vez

        for idx, (comunidad_id, nodos) in enumerate(comunidades.items()):
            intereses_comunidad = []

            # Extrae los intereses de los nodos dentro de la comunidad
            for nodo in nodos:
                if "intereses" in self.G.nodes[nodo]:
                    intereses_comunidad.extend(self.G.nodes[nodo]["intereses"])
            
            # Asigna un nombre a la comunidad basado en intereses o nombres genéricos
            if not comunidad_asignada and interes_seleccionado and interes_seleccionado in (i.lower() for i in intereses_comunidad):
                nombre_comunidad = f"Comunidad de {interes_seleccionado.capitalize()}"
                comunidad_asignada = True  # Evita repetir el nombre
            elif intereses_comunidad:
                nombre_comunidad = f"Comunidad de {Counter(intereses_comunidad).most_common(1)[0][0]}"
            else:
                nombre_comunidad = nombres_generales[idx % len(nombres_generales)]

            comunidades_nombradas[nombre_comunidad] = nodos
            comunidad_mapping[comunidad_id] = nombre_comunidad

            # Asigna la comunidad a los nodos dentro del grafo
            for nodo in nodos:
                self.G.nodes[nodo]["comunidad"] = nombre_comunidad  

            print(f"Comunidad '{nombre_comunidad}' tiene los intereses: {intereses_comunidad}")
        
        return comunidades_nombradas, comunidad_mapping

    def draw_graph(self, G=None, fig_size=(7, 4), node_size=320, communities=False, comunidad_mapping=None):
        if G is None:
            G = self.G  # Usa el grafo principal si no se proporciona otro
        
        pos = nx.spring_layout(self.G)  # Calcula la disposición de los nodos
        fig, ax = plt.subplots(figsize=fig_size)

        if communities:
            # Obtiene la partición de comunidades
            partition = community_louvain.best_partition(self.G)
            community_names, comunidad_mapping = self.detect_communities()
            
            # Asigna un color único a cada comunidad
            comunidad_colors = {comunidad_id: i for i, comunidad_id in enumerate(set(partition.values()))}
            
            unique_communities = set(comunidad_mapping.values())
            color_dict = {comunidad: plt.cm.Set3(i) for i, comunidad in enumerate(unique_communities)}
            
            # Asigna colores a los nodos según la comunidad a la que pertenecen
            color_map = [color_dict[self.G.nodes[n]["comunidad"]] if "comunidad" in self.G.nodes[n] else "gray" for n in self.G.nodes]
            
            # Crea la leyenda para las comunidades
            handles = [
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_dict[comunidad], markersize=10) 
                for comunidad in unique_communities
            ]
            ax.legend(handles, unique_communities, title="Comunidades", fontsize="small", frameon=False)
        else:
            # Si no hay comunidades, colorea los nodos según su tipo
            color_map = ["blue" if self.G.nodes[n]["tipo"] == "Estudiante" else "red" for n in self.G.nodes]
        
        nx.draw(self.G, pos, with_labels=True, node_color=color_map, ax=ax, node_size=node_size, cmap=plt.cm.Set3)
        return fig
