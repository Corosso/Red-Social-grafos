import networkx as nx
import matplotlib.pyplot as plt
import community as community_louvain
from collections import Counter

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
    def buscar_y_filtrar(self, interes):
        """
        Filtra y muestra el grafo basado en un interés específico.
        
        Parámetros:
        - interes (str): El interés por el cual se filtrarán los nodos.
        
        Retorna:
        - nx.Graph: El grafo filtrado.
        """
        # Obtener el grafo filtrado
        G_filtrado = self.get_filtered_graph(interes, self.perfiles, self.colaboraciones)

        # Verificar si hay nodos en el grafo filtrado
        if len(G_filtrado.nodes) == 0:
            print(f"No se encontraron nodos con el interés: {interes}")
            return None

        # Dibujar el grafo filtrado
        self.draw_graph(G_filtrado, fig_size=(6, 4), node_size=300, communities=True)

        return G_filtrado

    def detect_communities(self):
        partition = community_louvain.best_partition(self.G)

        # Agrupar nodos por comunidad
        comunidades = {}
        for nodo, comunidad_id in partition.items():
            if comunidad_id not in comunidades:
                comunidades[comunidad_id] = []
            comunidades[comunidad_id].append(nodo)

        # Diccionario para nombres personalizados de comunidades
        nombres_generales = ["Comunidad de Estudio", "Comunidad de Investigación", "Comunidad de Tesis", 
                            "Comunidad de Proyectos", "Comunidad de Redes", "Comunidad Académica"]

        comunidades_nombradas = {}
        for idx, (comunidad_id, nodos) in enumerate(comunidades.items()):
            intereses = []

            # Extraer intereses de los nodos en la comunidad
            for nodo in nodos:
                if "intereses" in self.G.nodes[nodo]:  # Verifica que el nodo tenga intereses
                    intereses.extend(self.G.nodes[nodo]["intereses"])  # Agrega los intereses del nodo

            # Determinar el interés más común en la comunidad
            if intereses:
                nombre_comunidad = Counter(intereses).most_common(1)[0][0]  # Toma el interés más repetido
            else:
                # Si no hay intereses, asigna un nombre predefinido
                nombre_comunidad = nombres_generales[idx % len(nombres_generales)]

            comunidades_nombradas[nombre_comunidad] = nodos

            # Debug: Mostrar en consola los intereses analizados
            print(f"Comunidad '{nombre_comunidad}' tiene los intereses: {intereses}")

        return comunidades_nombradas
    
    """
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
    """       
    def draw_graph(self, G=None, fig_size=(6, 4), node_size=300, communities=False):
        if G is None:
            G = self.G  # Usa el grafo principal si no se pasa uno
   
        #Dibuja el grafo con la opción de resaltar comunidades y ajustar el tamaño de los nodos.
        
        #Parámetros:
        #fig_size (tuple): Tamaño de la figura en pulgadas (ancho, alto).
        #node_size (int): Tamaño de los nodos en la visualización.
        #communities (bool): Si es True, colorea los nodos según su comunidad.
        
        #Retorna:
        #matplotlib.figure.Figure: Figura generada para la visualización del grafo.
        
        pos = nx.spring_layout(self.G)  # Layout para distribuir los nodos
        print("fig_size:", fig_size, type(fig_size))
        fig, ax = plt.subplots(figsize=fig_size)

        if communities:
            partition = community_louvain.best_partition(self.G)
            comunidad_colors = {comunidad_id: i for i, comunidad_id in enumerate(set(partition.values()))}
            color_map = [comunidad_colors[partition[n]] for n in self.G.nodes]
        else:
            color_map = ["blue" if self.G.nodes[n]["tipo"] == "Estudiante" else "red" for n in self.G.nodes]

        nx.draw(self.G, pos, with_labels=True, node_color=color_map, ax=ax, node_size=node_size, cmap=plt.cm.Set3)
        return fig