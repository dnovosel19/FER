import networkx as nx
import matplotlib.pylab as plt
import sys

def provjera_ciklusa(trenutni_graf, v1, v2):    # provjera ako dodamo neki brid hoce li se stvoriti ciklus
    closed = set()  # vrh je dodan u stablo
    closed.add(v1)
    skup_provjere = set()
    skup_provjere.add(v1)
    while True:
        pomoc = set()
        for i in trenutni_graf:     
            for j in skup_provjere: # dodajemo susjede od svih vec pronadenih vrhova, pretrazivanje u sirinu
                if (i[0] == j):
                    pomoc.add(i[1])
                elif (i[1] == j):
                    pomoc.add(i[0])
        skup_provjere.clear()
        for i in pomoc:     # iteriramo po pronadenim susjedima trenutnih vrhova
            if i == v2:     # ako je jedan od tih vrhova takoder vrh koji smo namjeravali dodati, onda zatvaramo ciklus
                return False
            if i not in closed: # ako vrh jos nismo stavili u stablo
                closed.add(i)
                skup_provjere.add(i)
        if len(skup_provjere) == 0: # prosli smo kroz sve vrhove i nismo pronasli ciklus
            return True

def KruskalMST(graph, vertex_edge):     # funkcija Kruskalovog algoritma 
    sorted_vertex_edge = sorted(vertex_edge, key=lambda x: x[2])    # sortiraj prema tezini bridova
    for i in sorted_vertex_edge:
        if provjera_ciklusa(graph, i[0], i[1]): # ako se ciklus ne stvara, onda ga dodaj u graf
            graph.append((i[0], i[1], i[2]))
        else:
            continue

def nacrtaj_graf(graph):    # funkcija za iscrtavanje grafa
    ispis = []
    for i in graph:     # (vrh1, vrh2, tezina_brida_vrh1_vrh2)
        ispis.append((i[0], i[1], {'weight': i[2]}))

    G = nx.Graph()
    G.add_edges_from(ispis)

    # pozicioniranje tocaka na grafu
    pos = {0: (0,0), 1: (1, 0.5), 7: (1, -0.5), 6: (2, -0.5), 2: (2, 0.5), 8: (2, 0), 3: (3, 0.5), 5: (3, -0.5), 4: (4, 0)}

    nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=12, font_weight="bold")

    edge_labels = nx.get_edge_attributes(G, 'weight')
    label_pos = {k: (v[0], v[1]) for k, v in pos.items()}
    nx.draw_networkx_edge_labels(G, label_pos, edge_labels=edge_labels, rotate=0)
    plt.show()

if __name__ == '__main__':
    vertex_edge = []    # izgled pocetnog grafa
    razdvoji_unos = sys.argv[1:]

    if len(razdvoji_unos) % 3 != 0: 
        print("Krivi unos parametara")
        exit()
    
    for i, unos in enumerate(razdvoji_unos):    # ucitavanje podataka
        if (i+1)%3 == 0:
            vertex_edge.append((int(razdvoji_unos[i-2]), int(razdvoji_unos[i-1]), int(razdvoji_unos[i])))

    graph = []  # pamti izgled konacnog grafa

    KruskalMST(graph, vertex_edge)
    print(graph)
    suma = 0
    for i in graph:
        suma += i[2]
    print(suma)
    nacrtaj_graf(graph)