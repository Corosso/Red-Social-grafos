"""
import networkx as nx
import matplotlib.pyplot as plt
import community as community_louvain
import numpy as np

class SocialGraph:
    def __init__(self):
        self.G = nx.Graph()
        
    def add_node(self, nombre, datos):
        self.G.add_node(nombre, tipo=datos["tipo"])
        
    def add_edge(self, nodo1, nodo2):
        self.G.add_edges_from([(nodo1, nodo2)])
        
    def remove_edge(self, nodo1, nodo2):
        self.G.remove_edge(nodo1, nodo2)
        
    
    def get_filtered_graph(self, interes, perfiles, colaboraciones):
        resultados = {nombre for nombre, datos in perfiles.items() if interes in datos["intereses"]}
    
        # Agregar los nodos que tienen el interés
        G_filtrado = nx.Graph()
        for nombre in resultados:
            G_filtrado.add_node(nombre, tipo=perfiles[nombre]["tipo"])

        # Mantener conexiones entre interesados y sus vecinos
        for n1, n2 in colaboraciones:
            if n1 in resultados or n2 in resultados:
                G_filtrado.add_node(n1, tipo=perfiles[n1]["tipo"])  # Asegurar que el nodo está en el grafo
                G_filtrado.add_node(n2, tipo=perfiles[n2]["tipo"])
                G_filtrado.add_edge(n1, n2)
        return G_filtrado


    def detect_communities(self):
        partition = community_louvain.best_partition(self.G)  # Detecta las comunidades
        return partition
        
    def draw_graph(self, fig_size=(6, 4), communities=False):

            pos = nx.spring_layout(self.G)
            fig, ax = plt.subplots(figsize=fig_size)

            # Si comunidades est� activado, asignamos colores por comunidad
            if communities:
                partition = self.detect_communities()
                color_map = [partition[node] for node in self.G.nodes]
            else:
                color_map = ["blue" if self.G.nodes[n]["tipo"] == "Estudiante" 
                             else "red" for n in self.G.nodes]

            nx.draw(self.G, pos, with_labels=True, node_color=color_map, 
                    ax=ax, node_size=2000)
            return fig
"""

import networkx as nx
import matplotlib.pyplot as plt
import community as community_louvain

class SocialGraph:
    def __init__(self):
        self.G = nx.Graph()
        
    def add_node(self, nombre, datos):
        """Agrega un nodo al grafo"""
        self.G.add_node(nombre, tipo=datos["tipo"])
        
    def add_edge(self, nodo1, nodo2):
        """Agrega una arista entre dos nodos"""
        self.G.add_edge(nodo1, nodo2)
        
    def remove_edge(self, nodo1, nodo2):
        """Elimina una arista entre dos nodos"""
        self.G.remove_edge(nodo1, nodo2)
        
    def get_filtered_graph(self, interes, perfiles, colaboraciones):
        """Filtra el grafo según el interés"""
        resultados = {nombre for nombre, datos in perfiles.items() if interes in datos["intereses"]}
    
        # Crear el grafo filtrado
        G_filtrado = nx.Graph()
        for nombre in resultados:
            G_filtrado.add_node(nombre, tipo=perfiles[nombre]["tipo"])

        # Mantener conexiones entre interesados y sus vecinos
        for n1, n2 in colaboraciones:
            if n1 in resultados or n2 in resultados:
                G_filtrado.add_node(n1, tipo=perfiles[n1]["tipo"])  # Asegurar que el nodo está en el grafo
                G_filtrado.add_node(n2, tipo=perfiles[n2]["tipo"])
                G_filtrado.add_edge(n1, n2)
        return G_filtrado

    def detect_communities(self):
        """Detecta comunidades en el grafo y las devuelve agrupadas"""
        partition = community_louvain.best_partition(self.G)

        # Agrupar nodos por comunidad
        comunidades = {}
        for nodo, comunidad_id in partition.items():
            if comunidad_id not in comunidades:
                comunidades[comunidad_id] = []
            comunidades[comunidad_id].append(nodo)

        return comunidades
        
    def draw_graph(self, fig_size=(6, 4), communities=False):
        """Dibuja el grafo con opción de mostrar comunidades"""
        pos = nx.spring_layout(self.G)
        fig, ax = plt.subplots(figsize=fig_size)

        if communities:
            partition = community_louvain.best_partition(self.G)
            comunidad_colors = {comunidad_id: i for i, comunidad_id in enumerate(set(partition.values()))}
            color_map = [comunidad_colors[partition[n]] for n in self.G.nodes]
        else:
            color_map = ["blue" if self.G.nodes[n]["tipo"] == "Estudiante" else "red" for n in self.G.nodes]

        nx.draw(self.G, pos, with_labels=True, node_color=color_map, ax=ax, node_size=2000, cmap=plt.cm.Set3)
        return fig
