import networkx as nx
import re
import matplotlib.pyplot as plt
import numpy as np

__author__ = 'fhca'


preposiciones = ['a', 'ante', 'bajo', 'con', 'contra', 'de', 'desde', 'en', 'entre', 'para', 'por', 'sin', 'segun',
                 'sobre', 'tras']
articulos = ['el', 'la', 'los', 'las', 'un', 'uno', 'unos', 'unas', 'ellos', 'ellas', 'esto', 'esta',
             'estos', 'estas', 'nosotras', 'nosotros', 'ustedes']
personajes = ['harry', 'hermione', 'ron', 'hagrid', 'dumbledore', 'malfoy']
removed = []
removed.extend(preposiciones)
removed.extend(articulos)


def splitting(filename):
    fd = open(filename, 'r')
    words = re.compile(r'\W')
    dots = re.compile(r'\.')
    start = True
    for line in fd:
        for phrase in dots.split(line):
            phrase_list = list(filter(''.__ne__, words.split(phrase)))
            if phrase_list and start:
                yield [x.lower() for x in phrase_list]


def palabras_consecutivas(filename):
    G = nx.DiGraph()
    for phrase in splitting(filename):
        for a, b in zip(phrase, phrase[1:]):
            G.add_edge(a, b)
    G.remove_nodes_from(removed)
    return G


def personajes_relacionados(filename):
    G = nx.DiGraph()
    for a in personajes:
        for b in personajes:
            if a != b:
                G.add_edge(a, b, relacionado=0)
    relaciones = [[w for w in phrase if w in personajes] for phrase in splitting(filename)]
    for rel in relaciones:
        # CRITERIO: si en una frase aparecen al menos dos personajes, entonces incrementa
        # la relación del 1ero con los demás.
        for p in personajes:
            if p in rel:
                G.node[p]['tam_nodo'] = G.node[p].get('tam_nodo', 0)+1
        if len(rel) >= 2:
            for otro in rel[1:]:
                if rel[0] != otro:
                    G[rel[0]][otro]["relacionado"] += 1
    # si no hubo relación, borra arista entre dos personajes
    print(filename)
    for e in G.edges():
        if G[e[0]][e[1]]["relacionado"] < 10:
            G.remove_edge(e[0], e[1])
        else:
            print("{} -> {} : {}".format(e[0], e[1], G[e[0]][e[1]]["relacionado"]))
    return G


def misma_frase(filename):
    G = nx.Graph()
    for phrase in splitting(filename):
        for a, b in zip(phrase, phrase[1:]):
            G.add_edge(a, b)
    return G
# G = palabras_consecutivas(file)
# G = misma_frase(file)

plt.figure(figsize=(12, 12))


def grafica(file):
    G = personajes_relacionados(file)
    # pos = nx.circular_layout(G)
    pos = nx.spring_layout(G, iterations=2)

    width_list = np.array([d['relacionado'] for _, _, d in G.edges(data=True)])
    tam_nodo = np.array([d['tam_nodo'] for _, d in G.nodes(data=True)])

    nx.draw_networkx_nodes(G, pos, label=True, node_size=tam_nodo, alpha=.5)
    nx.draw_networkx_edges(G, pos, alpha=.3, edge_color=width_list*30,
                           width=width_list/20)
    nx.draw_networkx_labels(G, pos, fontsize=14, font_color="g")
    plt.xticks([])
    plt.yticks([])
    plt.title(file)

plt.subplots_adjust(bottom=0.025, left=0.025, top=0.975, right=0.975)
plt.subplot(221)
grafica("L1piedra.txt")
plt.subplot(222)
grafica("L2camara.txt")
plt.subplot(223)
grafica("L3azkaban.txt")
plt.subplot(224)
grafica("L4caliz.txt")

plt.show()
