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
            for j in skup_provjere:     # dodajemo susjede od svih vec pronadenih vrhova, pretrazivanje u sirinu
                if (i[0] == j):
                    pomoc.add(i[1])
                elif (i[1] == j):
                    pomoc.add(i[0])
        skup_provjere.clear()
        for i in pomoc:     # iteriramo po pronadenim susjedima trenutnih vrhova
            if i == v2:     # ako je jedan od tih vrhova takoder vrh koji smo namjeravali dodati, onda zatvaramo ciklus
                return False
            if i not in closed:     # ako vrh jos nismo stavili u stablo
                closed.add(i)
                skup_provjere.add(i)
        if len(skup_provjere) == 0:     # prosli smo kroz sve vrhove i nismo pronasli ciklus
            return True
        
def PrimMST(graph, vertex_edge, pocetak):   # Primov algoritam
    closed = set()
    closed.add(pocetak)
    open = []
    while True:
        for i in vertex_edge:       # prolazak po bridovima, ali samo od onog zadnjeg dodanog vrha
            if (i[0] == pocetak) and (i[1] not in closed):
                open.append(i)
            if (i[1] == pocetak) and (i[0] not in closed):
                open.append(i)
        sorted_open = sorted(open, key=lambda x: x[2])  # sortiraj bridove tog vrha prema tezini
        index = []
        for ind, i in enumerate(sorted_open):   # provjera novih bridova
            if provjera_ciklusa(graph, i[0], i[1]):     # ako ne zatvara ciklus izvrsavaj
                graph.append((i[0], i[1], i[2]))
                index.append(ind)
                if i[0] not in closed:
                    pocetak = i[0]
                    closed.add(i[0])
                elif i[1] not in closed:
                    closed.add(i[1])
                    pocetak = i[1]
                break
            else:       # ako brid zatvara ciklus, ukloni ga
                index.append(ind)
                continue
        index.reverse()
        for i in index:
            sorted_open.pop(i)
        open = sorted_open
        if len(open) == 0:  # ako smo prosli po svim vrhovima, izadi
            break

def nacrtaj_graf(graph):    # funkcija za iscrtavanje grafa
    ispis = []
    for i in graph:     # (vrh1, vrh2, tezina_brida_vrh1_vrh2)
        ispis.append((i[0], i[1], {'weight': i[2]}))

    G = nx.Graph()
    G.add_edges_from(ispis)

    # pozicioniranje tocaka na grafu
    pos = {0: (0,0), 1: (1, 0.5), 7: (1, -0.5), 6: (2, -0.5), 8: (2, 0.5), 2: (2, 0), 3: (3, 0.5), 5: (3, -0.5), 4: (4, 0)}

    nx.draw(G, pos, with_labels=True, node_size=1000, node_color="skyblue", font_size=12, font_weight="bold")

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

    PrimMST(graph, vertex_edge, 0)
    print(graph)
    suma = 0
    for i in graph:
        suma += i[2]
    print(suma)
    nacrtaj_graf(graph)