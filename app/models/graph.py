import networkx as nx
import matplotlib.pyplot as plt
import community as community_louvain

class SocialGraph:
    
    #Clase que representa un grafo social utilizando NetworkX.
    #El grafo es no dirigido y permite la adición de nodos y aristas,
    #filtrado por intereses, detección de comunidades y visualización.
    
    def __init__(self):
        #Inicializa un grafo no dirigido.
        self.G = nx.Graph()
        
    def add_node(self, nombre, datos):
        
        #Agrega un nodo al grafo.
        
        #Parámetros:
        #nombre (str): Identificador único del nodo.
        #datos (dict): Diccionario con información del nodo, incluyendo su tipo.
        
        self.G.add_node(nombre, tipo=datos["tipo"])
        
    def add_edge(self, nodo1, nodo2):
        
        #Agrega una arista entre dos nodos en el grafo.
        
        #Parámetros:
        #nodo1 (str): Primer nodo.
        #nodo2 (str): Segundo nodo.
        
        self.G.add_edge(nodo1, nodo2)
        
    def remove_edge(self, nodo1, nodo2):
        
        #Elimina una arista entre dos nodos si existe.
        
        #Parámetros:
        #nodo1 (str): Primer nodo.
        #nodo2 (str): Segundo nodo.
        
        self.G.remove_edge(nodo1, nodo2)
        
    def get_filtered_graph(self, interes, perfiles, colaboraciones):
        
        #Filtra el grafo con base en un interés específico.
        
        #Parámetros:
        #interes (str): Interés por el cual filtrar los nodos.
        #perfiles (dict): Diccionario de perfiles con sus intereses y tipo.
        #colaboraciones (list): Lista de tuplas representando conexiones entre nodos.
        
        #Retorna:
        #nx.Graph: Un nuevo grafo solo con los nodos y conexiones relevantes.
        
        # Filtrar los nodos que tienen el interés especificado
        resultados = {nombre for nombre, datos in perfiles.items() if interes in datos["intereses"]}
    
        # Crear un nuevo grafo filtrado
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
        
        #Detecta comunidades en el grafo utilizando el algoritmo de Louvain.
        
        #Retorna:
        #dict: Un diccionario con comunidades donde las claves son los IDs de comunidad
        #y los valores son listas de nodos pertenecientes a cada comunidad.
        
        partition = community_louvain.best_partition(self.G)

        # Agrupar nodos por comunidad
        comunidades = {}
        for nodo, comunidad_id in partition.items():
            if comunidad_id not in comunidades:
                comunidades[comunidad_id] = []
            comunidades[comunidad_id].append(nodo)

        return comunidades
        
    def draw_graph(self, fig_size=(6, 4), node_size=300, communities=False):
        
        #Dibuja el grafo con la opción de resaltar comunidades y ajustar el tamaño de los nodos.
        
        #Parámetros:
        #fig_size (tuple): Tamaño de la figura en pulgadas (ancho, alto).
        #node_size (int): Tamaño de los nodos en la visualización.
        #communities (bool): Si es True, colorea los nodos según su comunidad.
        
        #Retorna:
        #matplotlib.figure.Figure: Figura generada para la visualización del grafo.
        
        pos = nx.spring_layout(self.G)  # Layout para distribuir los nodos
        fig, ax = plt.subplots(figsize=fig_size)

        if communities:
            partition = community_louvain.best_partition(self.G)
            comunidad_colors = {comunidad_id: i for i, comunidad_id in enumerate(set(partition.values()))}
            color_map = [comunidad_colors[partition[n]] for n in self.G.nodes]
        else:
            color_map = ["blue" if self.G.nodes[n]["tipo"] == "Estudiante" else "red" for n in self.G.nodes]

        nx.draw(self.G, pos, with_labels=True, node_color=color_map, ax=ax, node_size=node_size, cmap=plt.cm.Set3)
        return fig