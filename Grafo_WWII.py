import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

aliados = [
    "Estados Unidos", "Reino Unido", "União Soviética",
    "França", "China", "Canadá", "Austrália"
]

eixo = [
    "Alemanha", "Itália", "Japão",
    "Hungria", "Romênia", "Bulgária"
]

aliancas = [
    # Aliados entre si
    ("Estados Unidos", "Reino Unido"),
    ("Estados Unidos", "União Soviética"),
    ("Estados Unidos", "França"),
    ("Estados Unidos", "China"),
    ("Estados Unidos", "Canadá"),
    ("Estados Unidos", "Austrália"),
    ("Reino Unido", "França"),
    ("Reino Unido", "União Soviética"),
    ("Reino Unido", "Canadá"),
    ("Reino Unido", "Austrália"),
    ("França", "União Soviética"),
    ("União Soviética", "China"),

    # Eixo entre si
    ("Alemanha", "Itália"),
    ("Alemanha", "Japão"),
    ("Alemanha", "Hungria"),
    ("Alemanha", "Romênia"),
    ("Alemanha", "Bulgária"),
    ("Itália", "Japão"),
    ("Itália", "Hungria"),
    ("Japão", "Hungria"),
    ("Hungria", "Romênia"),
    ("Romênia", "Bulgária")
]

conflitos = [
    # Aliados vs Eixo
    ("Estados Unidos", "Alemanha"),
    ("Estados Unidos", "Japão"),
    ("Estados Unidos", "Itália"),
    ("Reino Unido", "Alemanha"),
    ("Reino Unido", "Itália"),
    ("Reino Unido", "Japão"),
    ("França", "Alemanha"),
    ("União Soviética", "Alemanha"),
    ("China", "Japão"),
    ("Canadá", "Alemanha"),
    ("Austrália", "Japão")
]


# CRIAÇÃO DO GRAFO:

# Criar grafo não direcionado
G = nx.Graph()

# Adicionar arestas de alianças (peso 1)
for u, v in aliancas:
    G.add_edge(u, v, weight=1)

# Adicionar arestas de conflitos (peso 2)
for u, v in conflitos:
    G.add_edge(u, v, weight=2)

for pais in G.nodes:
    if pais in aliados:
        G.nodes[pais]['grupo'] = 'Aliados'
    else:
        G.nodes[pais]['grupo'] = 'Eixo'

cores_nos = []
for pais in G.nodes:
    grupo = G.nodes[pais]['grupo']
    if grupo == 'Aliados':
        cores_nos.append("blue")
    else:
        cores_nos.append("yellow")



# CRIAÇÃO DA MATRIZ DE ADJACÊNCIA:

nos = list(G.nodes)

# Criando a matriz
matriz = np.zeros((len(nos), len(nos)))

# Preencheendo com os pesos das arestas
for i, origem in enumerate(nos):
    for j, destino in enumerate(nos):
        if G.has_edge(origem, destino):
            matriz[i][j] = G[origem][destino]['weight']
        else:
            matriz[i][j] = 0

# Exibindo
print("Matriz de Adjacência (com pesos):")
print(matriz)

print(" ")
print(" ")



# MÉTRICAS:

# Grau dos nós
graus = dict(G.degree())
print("Grau dos nós:")
print(graus)

# Centralidades
print("\nCentralidade de Grau:")
print(nx.degree_centrality(G))

print("\nCentralidade de Proximidade:")
print(nx.closeness_centrality(G))

print("\nCentralidade de vetor próprio:")
centralidade_vetor_proprio = nx.eigenvector_centrality(G, weight='weight')
for pais, valor in centralidade_vetor_proprio.items():
    print(f"{pais}: {valor:.4f}")
print(" ")

# Densidade da rede
componentes = list(nx.connected_components(G))
densidade = nx.density(G)
print(f"Densidade da rede: {densidade:.4f}")
print (" ")

# Diâmetro da maior componente
maior_componente = max(componentes, key=len)
subgrafo = G.subgraph(maior_componente)
print("\nDiâmetro da rede (maior componente):", nx.diameter(subgrafo))
print(" ")




# ALGORITMOS PARA ANÁLISE DO GRAFO (BFS e DFS):

# BFS
caminho_bfs = nx.shortest_path(G, source="China", target="Bulgária")
passos_bfs = len(caminho_bfs) - 1
print("Caminho (BFS):", caminho_bfs)
print("Número de passos:", passos_bfs)
print(" ")

# DFS
def dfs(grafo, inicio, visitados=None):
    if visitados is None:
        visitados = set()

    visitados.add(inicio)
    print(inicio)

    for vizinho in grafo.neighbors(inicio):
        if vizinho not in visitados:
            dfs(grafo, vizinho, visitados)
print("Busca em profundidade (DFS) a partir de 'Estados Unidos':")
dfs(G, "Estados Unidos")



# CRIAÇÃO DA PARTE GRÁFICA DO GRAFO:

# Cores diferentes para aliados e inimigos
cores_arestas = ['green' if G[u][v]['weight'] == 1 else 'red' for u, v in G.edges]

# Layout e desenho
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True,
        node_color=cores_nos,
        edge_color=cores_arestas,
        font_size=8, node_size=1000)

# Rótulos de peso nas arestas
#edge_labels = nx.get_edge_attributes(G, 'weight')
#nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='gray')

# Legenda
legenda = [
    Patch(color='blue', label='Aliados'),
    Patch(color='yellow', label='Eixo'),
    Patch(color='green', label='Aliança (peso 1)'),
    Patch(color='red', label='Conflito (peso 2)')
]

plt.legend(handles=legenda, loc='upper left', bbox_to_anchor=(1, 1))
plt.title("Relações entre Países na Segunda Guerra Mundial")
plt.tight_layout()
plt.show()