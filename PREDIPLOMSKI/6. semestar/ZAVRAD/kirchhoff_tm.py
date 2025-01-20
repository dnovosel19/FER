import sys

def stvori_matricu(matrix, n, bridovi):     # funkcija za izradu matrice susjedstva
    for i in range(n):  # stvaramo praznu matricu
        red = []
        for j in range(n):
            red.append(0)
        matrix.append(red)
    for i in bridovi:   # u praznu matricu upisujemo 1 ako su vrhovi spojeni
        matrix[i[0] - 1][i[1] - 1] = 1
        matrix[i[1] - 1][i[0] - 1] = 1

def preoblikuj_matricu(matrix):     # promijeni matricu tako da na dijagonalu upises broj povezanih vrhova s nekim cvorom te sve ne-dijagonalne elemente (razlicite od 0) zamijeni s -1
    for ind, red in enumerate(matrix):
        degree_of_node = 0      # u svakom redu prebroji koliko je vrhova spojeno sa trenutnim
        for index, element in enumerate(red):
            degree_of_node += element
            if element == 1:
                matrix[ind][index] = -1
        matrix[ind][ind] = degree_of_node

def zbroji_retke(prvi_redak, drugi_redak, index_koji_postaje_nula): # funkcija koja zbraja dva retka matrice, pretvaramo stupac po stupac do gornje trokutastog oblika
    broj = (-1) * drugi_redak[index_koji_postaje_nula] / prvi_redak[index_koji_postaje_nula]    # formula kojom izracunamo s cime pomnoziti prvi redak kako bi u iducem ponistio jedan element
    novi_red = []
    for ind, i in enumerate(prvi_redak):
        for index, j in enumerate(drugi_redak):
            if ind == index:
                novi_red.append(i*broj + j)
    return novi_red

def izracunaj_broj_razapinjucih_stabala(matrix, x, y):  # rjesenje
    matrix.pop(x)   # makni red x i stupac y
    for red in matrix:
        del red[y]

    broj_koraka = len(matrix) - 1   # znamo u koliko koraka mozemo matricu dovesti u gornje trokutasti oblik
    trenutni_redak = 0

    for i in range(broj_koraka):
        for ind, red in enumerate(matrix):
            if ind < trenutni_redak:
                continue
            elif ind == trenutni_redak:
                redak = red
            elif ind > trenutni_redak:
                novi_redak = zbroji_retke(redak, red, trenutni_redak)
                matrix[ind] = novi_redak
        trenutni_redak += 1
    
    broj_stabala = 1
    for ind, i in enumerate(matrix):
        broj_stabala *= matrix[ind][ind]
    for i in matrix:
        print(i)
    print((broj_stabala))  # zaokruzi jer se ne koriste razlomci vec decimalni brojevi pa ce brojevi ispasti decimalni

if __name__ == '__main__':
    vertex_edge = []    # izgled pocetnog grafa
    razdvoji_unos = sys.argv[1:]
    
    if len(razdvoji_unos) % 2 != 0:     # ucitavanje podataka
        print("Krivi unos parametara")
        exit()
    
    for i, unos in enumerate(razdvoji_unos):
        if (i+1)%2 == 0:
            vertex_edge.append((int(razdvoji_unos[i-1]), int(razdvoji_unos[i])))

    pamti_vrhove = set()
    for i in vertex_edge:   # prebroji koliko je vrhova u zadanom grafu
        pamti_vrhove.add(i[0])
        pamti_vrhove.add(i[1])

    matrica = []

    stvori_matricu(matrica, len(pamti_vrhove), vertex_edge)

    preoblikuj_matricu(matrica)

    izracunaj_broj_razapinjucih_stabala(matrica, 0, 0)