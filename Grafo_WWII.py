import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

aliados = [
    "EUA", "UK", "URSS",
    "França", "China", "Canadá", "Austrália", "Brasil"
]

eixo = [
    "Alemanha", "Itália", "Japão",
    "Hungria", "Romênia", "Bulgária"
]

neutro = [
    "Suécia", "Suíça", "Turquia",
    "Espanha", "Irlanda", "Portugal"
]

aliancas = [
    # Aliados entre si
    ("EUA", "UK"),
    ("EUA", "URSS"),
    ("EUA", "França"),
    ("EUA", "China"),
    ("EUA", "Canadá"),
    ("EUA", "Austrália"),
    ("UK", "França"),
    ("UK", "URSS"),
    ("UK", "Canadá"),
    ("UK", "Austrália"),
    ("França", "URSS"),
    ("URSS", "China"),
    ("Brasil", "EUA"),

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
    ("EUA", "Alemanha"),
    ("EUA", "Japão"),
    ("EUA", "Itália"),
    ("UK", "Alemanha"),
    ("UK", "Itália"),
    ("UK", "Japão"),
    ("França", "Alemanha"),
    ("URSS", "Alemanha"),
    ("China", "Japão"),
    ("Canadá", "Alemanha"),
    ("Austrália", "Japão"),
    ("Brasil", "Itália"),
    ("Brasil", "Alemanha")
]

relacoes = [
    # Relações entre países neutros entre si e com participantes da guerra
    ("Suécia", "Alemanha"),
    ("Suécia", "UK"),
    ("Suíça", "Alemanha"),
    ("Suíça", "UK"),
    ("Suíça", "EUA"),
    ("Turquia", "UK"),
    ("Turquia", "Alemanha"),
    ("Turquia", "URSS"),
    ("Espanha", "Alemanha"),
    ("Espanha", "Itália"),
    ("Espanha", "Portugal"),
    ("Irlanda", "UK"),
    ("Irlanda", "EUA"),
    ("Portugal", "UK"),
    ("Portugal", "EUA"),
    ("Portugal", "Espanha")
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

# Adicionando arestas de relações neutras (peso 3)
for u, v in relacoes:
    G.add_edge(u, v, weight=3)

for pais in G.nodes:
    if pais in aliados:
        G.nodes[pais]['grupo'] = 'Aliados'
    elif pais in eixo:
        G.nodes[pais]['grupo'] = 'Eixo'
    else:
        G.nodes[pais]['grupo'] = 'Neutros'

cores_nos = []
for pais in G.nodes:
    grupo = G.nodes[pais]['grupo']
    if grupo == 'Aliados':
        cores_nos.append("blue")
    elif grupo == 'Eixo':
        cores_nos.append("darkred")
    else:
        cores_nos.append("grey")



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
print("Busca em profundidade (DFS) a partir de 'EUA':")
dfs(G, "EUA")



# CRIAÇÃO DA PARTE GRÁFICA DO GRAFO:

# Cores diferentes para aliados e inimigos
cores_arestas = []

for u, v in G.edges:
    peso = G[u][v]['weight']
    if peso == 1:
        cores_arestas.append('green')
    elif peso == 2:
        cores_arestas.append('red')
    else:
        cores_arestas.append('black')

# Layout e desenho
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True,
        node_color=cores_nos,
        edge_color=cores_arestas,
        font_size=8, node_size=1000,
        font_color='yellow')

# Rótulos de peso nas arestas
#edge_labels = nx.get_edge_attributes(G, 'weight')
#nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='gray')

# Legenda
legenda_nos = [
    mpatches.Patch(color='blue', label='Aliados'),
    mpatches.Patch(color='darkred', label='Eixo'),
    mpatches.Patch(color='gray', label='Neutros')
]

legenda_arestas = [
    Line2D([0], [0], color='green', lw=2, label='Aliança'),
    Line2D([0], [0], color='red', lw=2, label='Conflito'),
    Line2D([0], [0], color='black', lw=2, label='Relação estratégica/neutra')
]

plt.legend(handles=legenda_arestas + legenda_nos, loc='lower left', frameon=True)
plt.title("Relações entre Países na Segunda Guerra Mundial")
#plt.tight_layout()
plt.show()