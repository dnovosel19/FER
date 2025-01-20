import sys
import heapq


# funkcija expand za bfs
def expand(n, broj, open, total_cost, pamti_dij_rod, closed):
    int_broj = float(broj) + 1  # pamtim dubinu
    pomoc = 0                   # pamtim trenutnu sveukupnu cijenu
    for i in mapa[n]:
        if i.split(',')[0] not in closed:
            pamti_dij_rod.append((i.split(',')[0] , n))
            pomoc = int(total_cost) + int(i.split(',')[1])
            open.append(i.split(',')[0]+','+str(int_broj)+','+str(pomoc))

# algoritam bfs
def bfs(s0, goal, total_cost):
    closed = set()
    pamti_dijete_roditelja = []     # lista parova (dijete, roditelj)
    initial = str(s0)+',0,0'
    open = [initial]
    
    while len(open) != 0:
        n = open.pop(0)
        closed.add(n.split(',')[0])
        if n.split(',')[0] in goal:
            total_cost = n.split(',')[2]
            path = [n.split(',')[0]]
            zastavica = 0   # prati jesmo li dosli sa kraja na pocetak
            while True:
                for k in pamti_dijete_roditelja:
                    if k[0] == path[-1]:
                        path.append(k[1])
                        if path[-1] == s0:
                            zastavica = 1
                            break
                if zastavica == 1:
                    break
            path.reverse()
            return 'yes', len(closed), len(path), total_cost, path

        total_cost = n.split(',')[2]
        expand(n.split(',')[0], n.split(',')[1], open, total_cost, pamti_dijete_roditelja, closed)
    return 'no', None, None, None, None

# funkcija expand za ucs
def expand_ucs(n, broj, open, pamti_dij_rod, closed):
    float_broj = float(broj)    # pamti dosadasnju cijenu puta
    for i in mapa[n]:
        ele = i.split(',')
        if ele[0] not in closed:
            pamti_dij_rod.append((ele[0] , n))
            pomoc = float_broj + float(ele[1])
            heapq.heappush(open, (pomoc, ele[0]))   # stavi par (cijena, cvor) unutar open, heapq ga sortira

# algoritam ucs
def ucs(s0, goal, total_cost, mapa):
    closed = set()
    pamti_dijete_roditelja = []     # lista parova (dijete, roditelj)
    initial = (0, s0)
    open = []
    heapq.heappush(open, initial)   # koristim heapq da ga pri ubacivanju u open sortira na najbrzi nacin
    closed_sa_brojkicama = set()
    
    while len(open) != 0:
        n = heapq.heappop(open)
        closed.add(n[1])
        closed_sa_brojkicama.add(str(n[1]) + ',' + str(n[0]))   # isto kao closed samo ovdje sluzi za pamcenje cvora i cijene
        
        if n[1] in goal:
            total_cost = n[0]
            path = [n[1]]
            zastavica = 0
            # petlja za trazenje predzadnjeg elementa path-a
            while True:
                for k in pamti_dijete_roditelja:        # trazi po listi (element, prethodnik)
                    if k[0] == path[-1]:
                        for prethodnik in closed_sa_brojkicama:     # trazi po closed listi
                            if (prethodnik.split(',')[0] == k[1]):  # ako je element u closed i prethodnik
                                valll = mapa[k[1]]                  # value od mape sa kljucem prethodnik
                                for nadi in valll:                  # iteracija po vrijednostima
                                    if nadi.split(',')[0] == path[-1]:  # provjeravamo ovo jer se moze dogoditi da nakon njega postoji jos neki par koji odgovara uvjetima (dogada se da zbog implementacije pamti_dijete_roditelja bez ovoga uvjeta dobijemo krivi path)
                                        if float(nadi.split(',')[1]) + float(prethodnik.split(',')[1]) == float(total_cost):    # provjera da je taj element zaista nas trazeni cvor, ako je onda ce cijena puta biti ista kao zbroj
                                            path.append(k[1])
                                            zastavica = 1
                                            break
                                if zastavica == 1:
                                    break
                        if zastavica == 1:
                            break
                if zastavica == 1:
                    break
            
            zastavica = 0
            while True:     # trazi ostale clanove path-a
                for k in pamti_dijete_roditelja:
                    if path[-1] == s0:
                        zastavica = 1
                        break
                    if k[0] == path[-1]:
                        path.append(k[1])
                        if path[-1] == s0:
                            zastavica = 1
                            break
                if zastavica == 1:
                    break
            path.reverse()
            return 'yes', len(closed), len(path), total_cost, path
        expand_ucs(n[1], n[0], open, pamti_dijete_roditelja, closed)
    return 'no', None, None, None, None

# algoritam A*
def astar(s0, goal, total_cost, mapa):
    initial = str(s0)+',0,0'
    open = [initial]
    closed = []
    pamti_dij_rod = []

    while len(open) != 0:
        n = open.pop(0)
        vec_postoji = -1
        for i, element in enumerate(closed):
            listica = element.split(',')
            if (listica[0] == n.split(',')[0]):
                vec_postoji = i
                break

        if vec_postoji == -1:   # ako nije u closed, onda ga stavi u closed na kraj 
            closed.append(n)
        else:
            if n.split(',')[1] < closed[vec_postoji]:   # ako vec postoji unutar closed te je put duzi nego od ovoga do kojeg smo dosli, onda ga makni iz closed 
                closed.pop(vec_postoji)
            else:                                       # ako je vrijednost veca ili jednaka kao vec zapisana onda samo ignoriraj
                continue

        if n.split(',')[0] in goal:
            total_cost = n.split(',')[2]
            path = [n.split(',')[0]]
            zastavica = 0

            # algoritam trazenja predzadnjeg cvora, algoritam ekvivalentan algoritmu unutar ucs-a
            while True:
                for k in pamti_dij_rod:
                    if k[0] == path[-1]:
                        for prethodnik in closed:
                            if (prethodnik.split(',')[0] == k[1]):
                                valll = mapa[k[1]]
                                for nadi in valll:
                                    if nadi.split(',')[0] == path[-1]:
                                        if float(nadi.split(',')[1]) + float(prethodnik.split(',')[1]) == float(total_cost):
                                            path.append(k[1])
                                            zastavica = 1
                                            break
                                if zastavica == 1:
                                    break
                        if zastavica == 1:
                            break
                if zastavica == 1:
                    break

            zastavica = 0
            while True:     # pronadi ostatak path-a
                for k in pamti_dij_rod:
                    if k[0] == path[-1]:
                        path.append(k[1])
                        if path[-1] == s0:
                            zastavica = 1
                            break
                if zastavica == 1:
                    break
            path.reverse()
            return 'yes', len(closed), len(path), total_cost, path

        float_broj = float(n.split(',')[1])
        # ekvivalentno pronalasku value unutar mape pomocu kljuca
        for i in bez_prijelaza:
            proba = i.split()
            if proba[0] == n.split(',')[0]+':':
                pamti = proba[1:]
                break

        for i in pamti:     # iteriraj po vrijednostima mape
            zastavica = 0
            postoji = 0
            if (i.split(',')[0], n.split(',')[0]) not in pamti_dij_rod:
                pamti_dij_rod.append((i.split(',')[0], n.split(',')[0]))
            indeks = 0
            ele = i.split(',')
            
            for k, el_closed in enumerate(closed):      # petlja gdje trazim ako je trenutni cvor manje cijene nego isti taj vec pronadeni, unutar closed
                listica = el_closed.split(',')
                if listica[0] == ele[0]:
                    postoji = 1
                if (listica[0] == ele[0]) and (float(listica[1]) > float(ele[1]) + float_broj):
                    closed.pop(k)
                    zastavica = 1
                    for ind, x in pamti_dij_rod:
                        if x[1] == listica[0]:
                            pamti_dij_rod.pop(ind)
                            break
                    break
                elif (listica[0] == ele[0]) and (float(listica[1]) <= float(ele[1]) + float_broj):
                    pamti_dij_rod.pop()
                    break

            for j, el_open in enumerate(open):          # petlja gdje trazim ako je trenutni cvor manje cijene nego isti taj vec pronadeni, unutar open
                listica = el_open.split(',')
                if listica[0] == ele[0]:
                    postoji = 1
                if (listica[0] == ele[0]) and (float(listica[1]) > float(ele[1]) + float_broj):
                    open.pop(j)
                    zastavica = 1
                    ind = 0
                    for x in pamti_dij_rod:
                        ind += 1
                        if x[1] == listica[0]:
                            pamti_dij_rod.pop(ind)
                            break
                    break
                elif (listica[0] == ele[0]) and (float(listica[1]) <= float(ele[1]) + float_broj):
                    pamti_dij_rod.pop()
                    break

            broj_bez_h = float_broj + float(ele[1])                     # cijena puta, bez uracunate heuristike
            broj_s_h = broj_bez_h + float(mapiram_heuristiku[ele[0]])   # uracunata heuristika
            stringic = ele[0]+','+str(broj_bez_h)+','+str(broj_s_h)     # string koji stavljamo unutar open

            if postoji == 0 or zastavica == 1:          # ako cvor ne postoji (prvi put smo naisli na njega) ili ako je postojao ali smo ga izbacili
                for umetni_element in open:
                    usporedivannje = float(umetni_element.split(',')[2])
                    if broj_s_h < usporedivannje:
                        break
                    if broj_s_h > usporedivannje:
                        indeks += 1
                    elif usporedivannje == broj_s_h:
                        if ele[0] > umetni_element.split(',')[0]:
                            indeks += 1
                            continue
                        elif ele[0] < umetni_element.split(',')[0]:
                            break
                if (indeks >= len(open)):       # ako je prosao sve unutar open, dodaj ga na kraj / tad je dobro sortirano
                    open.append(stringic)
                else:
                    open.insert(indeks, stringic)   # ako je manji od duljine open-a onda ga negdje treba umetnutu, imamo indeks iz gornje petlje koji zna gdje ga treba umetnuti
        
    return 'no', None, None, None, None

razdvoji_unos = sys.argv
mapiram_heuristiku = {}         # mapa nastala od file-a heuristike za brze pretrazivanje
zastavica_konzistentnosti = 0   # gledaj trazis li konzistentnost ili optimalnost
koji_alg = ""
bez_prijelaza = []
mapa = {}                       # mapa za ucitanu datoteku

for i in range(len(razdvoji_unos)):     # ucitavanje podataka

    if razdvoji_unos[i] == "--ss":
        ime_txt_file = razdvoji_unos[i + 1]
        try:
            with open(ime_txt_file, 'r', encoding='utf-8') as file:
                ucitan_file = file.readlines()
        except FileNotFoundError:
            print("Greska prilikom otvaranja datoteke.")

    if razdvoji_unos[i] == "--alg":
        koji_alg = razdvoji_unos[i + 1]

    if razdvoji_unos[i] == "--h":
        opisnik_heuristike = razdvoji_unos[i + 1]
        try:
            with open(opisnik_heuristike, 'r', encoding='utf-8') as file:
                heuristika = file.readlines()
        except FileNotFoundError:
            print("Greska prilikom otvaranja datoteke.")
        for line in heuristika:             # stvaramo mapu, kljuc je cvor, value je broj
            key, value = line.split(':')
            mapiram_heuristiku[key] = value

    if razdvoji_unos[i] == "--check-optimistic":
        zastavica_optimisticnosti = 1

    if razdvoji_unos[i] == "--check-consistent":
        zastavica_konzistentnosti = 1

br = 0      # varijabla koja sluzi za preskakanje prva dva ucitana podatka, oni nam ne trebaju za mapiranje
for i in ucitan_file:
    if i[0] != '#':     # preskacemo komentare
        bez_prijelaza.append(i.strip())
        br = br+1
        if br > 2:
            key = i.split(':')[0]
            val = i.split(':')[1]
            val1 = val.split()
            value = []
            for j in val1:
                value.append(j.split(',')[0] + ',' + j.split(',')[1])
                if koji_alg == "bfs":
                    value.sort()
            mapa[key] = val1


s0 = bez_prijelaza[0]           # pocetno stanje
goal = bez_prijelaza[1].split()     # ciljno stanje
total_cost = 0

ispis = ''

if koji_alg == "bfs":       # ako je algoritam bfs
    found_solution, states_visited, path_length, tot_cost, path = bfs(s0, goal, total_cost)
    if found_solution == 'yes':
        zaokruzi = "{:.1f}".format(float(tot_cost))     # broj koji je zaokruzen na jednu decimalu
        ispis += "# BFS\n[FOUND_SOLUTION]: " + found_solution + "\n[STATES_VISITED]: " + str(states_visited) + "\n[PATH_LENGTH]: " + str(path_length) + "\n[TOTAL_COST]: " + str(zaokruzi) + "\n[PATH]: "
        for i in range(len(path)):
            ispis += path[i]
            if i != len(path)-1:
                ispis += " => "
        print(ispis)
    else:
        print("# BFS\n[FOUND_SOLUTION]: no")

elif koji_alg == "ucs":     # ako je algoritam ucs
    found_solution, states_visited, path_length, tot_cost, path = ucs(s0, goal, total_cost, mapa)
    if found_solution == 'yes':
        zaokruzi = "{:.1f}".format(float(tot_cost))     # broj koji je zaokruzen na jednu decimalu
        ispis += "# UCS\n[FOUND_SOLUTION]: " + found_solution + "\n[STATES_VISITED]: " + str(states_visited) + "\n[PATH_LENGTH]: " + str(path_length) + "\n[TOTAL_COST]: " + str(zaokruzi) + "\n[PATH]: "
        for i in range(len(path)):
            ispis += path[i]
            if i != len(path)-1:
                ispis += " => "
        print(ispis)
    else:
        print("# UCS\n[FOUND_SOLUTION]: no")

elif koji_alg == "astar":   # ako je algoritam A*
    found_solution, states_visited, path_length, tot_cost, path = astar(s0, goal, total_cost, mapa)
    if found_solution == 'yes':
        zaokruzi = "{:.1f}".format(float(tot_cost))     # broj koji je zaokruzen na jednu decimalu
        ispis += "# A-STAR " + opisnik_heuristike + "\n[FOUND_SOLUTION]: " + found_solution + "\n[STATES_VISITED]: " + str(states_visited) + "\n[PATH_LENGTH]: " + str(path_length) + "\n[TOTAL_COST]: " + str(zaokruzi) + "\n[PATH]: "
        for i in range(len(path)):
            ispis += path[i]
            if i != len(path)-1:
                ispis += " => "
        print(ispis)
    else: 
        print("# A-STAR " + opisnik_heuristike + "\n[FOUND_SOLUTION]: no")

else:       # slucaj kada nije dan algoritam nego se ispituje heuristika
    sortirana_map_heur = dict(sorted(mapiram_heuristiku.items()))   # sortiraj mapu heuristike prema kljucu / ova linija koda je prilagodena na temelju stranice: https://www.freecodecamp.org/news/python-sort-dictionary-by-key/
    kraj = 1
    if zastavica_konzistentnosti == 1:      # provjera konzistentnosti
        ispis += "# HEURISTIC-CONSISTENT " + opisnik_heuristike + "\n"
        for element_heuristike in sortirana_map_heur:
            if element_heuristike not in goal:
                prvi_broj = float(sortirana_map_heur[element_heuristike])
            else:
                prvi_broj = float(0)
            listaa = mapa[element_heuristike]
            listaa.sort()
            for element_mape in listaa:
                treci_broj = float(element_mape.split(',')[1])
                drugi_broj = float(sortirana_map_heur[element_mape.split(',')[0]])
                if prvi_broj <= drugi_broj + treci_broj:
                    ispis += "[CONDITION]: [OK] h(" + element_heuristike + ") <= h(" + element_mape.split(',')[0] + ") + c: " + str(prvi_broj) + " <= " + str(drugi_broj) + " + " + str(treci_broj) + "\n"
                else:
                    kraj =0
                    ispis += "[CONDITION]: [ERR] h(" + element_heuristike + ") <= h(" + element_mape.split(',')[0] + ") + c: " + str(prvi_broj) + " <= " + str(drugi_broj) + " + " + str(treci_broj) + "\n"
        if kraj == 0:
            ispis += "[CONCLUSION]: Heuristic is not consistent."
        else:
            ispis += "[CONCLUSION]: Heuristic is consistent."
        print(ispis)
        
    else:           # provjera optimisticnosti
        ispis += "# HEURISTIC-OPTIMISTIC " + opisnik_heuristike + "\n"
        for element_heuristike in sortirana_map_heur:
            total_cost = 0
            if element_heuristike not in goal:
                found_solution, states_visited, path_length, tot_cost, path = ucs(element_heuristike, goal, total_cost, mapa)
                if tot_cost == None:
                    tot_cost = 0
                zaokruzi = "{:.1f}".format(float(mapiram_heuristiku[element_heuristike]))   # broj koji je zaokruzen na jednu decimalu
                if float(mapiram_heuristiku[element_heuristike]) <= float(tot_cost):
                    ispis += "[CONDITION]: [OK] h(" + element_heuristike + ") <= h*: " + zaokruzi + " <= " + str(tot_cost) + "\n"
                else:
                    kraj = 0
                    ispis += "[CONDITION]: [ERR] h(" + element_heuristike + ") <= h*: " + zaokruzi + " <= " + str(tot_cost) + "\n"
            else:
                ispis += "[CONDITION]: [OK] h(" + element_heuristike + ") <= h*: 0.0 <= 0.0\n"

        if kraj == 0:
            ispis += "[CONCLUSION]: Heuristic is not optimistic."
        else:
            ispis += "[CONCLUSION]: Heuristic is optimistic."
                
        print(ispis)