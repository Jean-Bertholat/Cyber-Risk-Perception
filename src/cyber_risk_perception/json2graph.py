import json
import networkx as nx
from pyvis.network import Network

# Fonction pour charger le fichier JSON depuis le serveur

def json2graph(data):

    data = json.loads(data)
    if data:
    # Créer un graphe NetworkX
        G = nx.Graph()

        # Ajouter les nœuds et les arêtes
        for item in data:
            risk = item["risk"]
            for consequence in item["consequences"]:
                G.add_edge(risk, consequence)

        # Initialiser le graphique PyVis
        net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white')

        # Ajouter le graphe NetworkX à PyVis
        net.from_nx(G)

        # Personnaliser l'apparence du graphe
        net.repulsion(node_distance=200)

        # Personnalisation du look du graphique
        net.set_options("""
        var options = {
            "nodes": {
                "color": {
                "border": "rgb(0,0,0)",
                "background": "rgb(150, 200, 255)"
                },
                "font": {
                "color": "black"
                },
                "size": 20
            },
            "edges": {
                "color": "rgb(0, 100, 200)",
                "width": 3,
                "smooth": {
                "type": "continuous"
                }
            },
            "physics": {
                "forceAtlas2Based": {
                "gravitationalConstant": -50,
                "centralGravity": 0.005,
                "springLength": 100,
                "springConstant": 0.08,
                "damping": 0.4
                },
                "solver": "forceAtlas2Based",
                "stabilization": {
                "enabled": true,
                "iterations": 200
                },
                "timestep": 0.5,
                "adaptiveTimestep": true
            }
        }""")

        # Sauvegarder le graphe dans un fichier HTML
        #net.show("graph_interactif.html", notebook=False)

    return net
