import networkx as nx
import matplotlib.pyplot as plt

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
        resultados = [nombre for nombre, datos in perfiles.items() 
                     if interes in datos["intereses"]]
        colaboraciones_filtradas = [(n1, n2) for n1, n2 in colaboraciones 
                                  if n1 in resultados or n2 in resultados]
        
        G_filtrado = nx.Graph()
        for nombre in resultados:
            G_filtrado.add_node(nombre, tipo=perfiles[nombre]["tipo"])
        G_filtrado.add_edges_from(colaboraciones_filtradas)
        
        return G_filtrado
        
    def draw_graph(self, fig_size=(6,4)):
        pos = nx.spring_layout(self.G)
        fig, ax = plt.subplots(figsize=fig_size)
        color_map = ["blue" if self.G.nodes[n]["tipo"] == "Estudiante" 
                    else "red" for n in self.G.nodes]
        nx.draw(self.G, pos, with_labels=True, node_color=color_map, 
                ax=ax, node_size=2000)
        return fig