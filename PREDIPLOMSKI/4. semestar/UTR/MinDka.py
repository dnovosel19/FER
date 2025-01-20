import sys

polje_redaka = []
for line in sys.stdin:
    polje_redaka.append(line)


dohvatljiva_stanja = []

def dfs(pocetno):
    if pocetno in dohvatljiva_stanja:
        return
    dohvatljiva_stanja.append(pocetno)
    for simb in skup_simbola_abecede:
        pomocni = pocetno + "," +simb
        dfs(prijelaz[pomocni])


stanja = polje_redaka[0].strip().split(",")

skup_simbola_abecede = polje_redaka[1].strip().split(",")

imam = len(polje_redaka[2])
if imam > 1:
    skup_prihvatljivih_stanja = polje_redaka[2].strip().split(",")
else:
    skup_prihvatljivih_stanja = []

ostala_stanja = []

pocetno_stanje = polje_redaka[3].strip()

for stanje in stanja:
    if stanje not in skup_prihvatljivih_stanja:
        ostala_stanja.append(stanje)

prijelaz = {}
for i in range(4, len(polje_redaka)):
    funk_prijelaza = polje_redaka[i].strip()
    fp_bez_strelice = funk_prijelaza.split("->")
    prijelaz[fp_bez_strelice[0]] = fp_bez_strelice[1]

grupe = []
grupe.append(skup_prihvatljivih_stanja)
grupe.append(ostala_stanja)

# Algoritam 2

while True:
    nove_grupe = grupe.copy()
    izlaz = len(grupe)
    for grupa in grupe: # idemo po grupama
        if len(grupa) > 1:
            pomocna1 = []
            pomocna2 = []
            pamti_grupe = []
            i = 0
            for clan1 in grupa: # uzmi jedan clan
                i = i + 1
                j = 0
                for clan2 in grupa: # uzmi drugi clan
                    j = j + 1
                    if i < j:
                        isti = True
                        if clan1 != clan2:  # iste ne gledamo
                            usporedba = []
                            for simbol in skup_simbola_abecede: # idemo po simbolima
                                pomoc1 = clan1 + ',' + simbol   # dobivamo kljuc od prijelaza
                                pomoc2 = clan2 + ',' + simbol   # dobivamo kljuc od prijelaza
                                
                                kopiraj_u_isto = []
                                kopiraj_u_razlicito = []
                                povratno = False
                                for jeli_u_istoj_grupi in grupe:    # podjela elemenata u dvije grupe
                                    if ((prijelaz[pomoc1] in jeli_u_istoj_grupi) and (prijelaz[pomoc2] in jeli_u_istoj_grupi)):
                                        povratno = True
                                        break

                                if povratno == True:
                                    if clan1 not in kopiraj_u_isto:
                                        kopiraj_u_isto.append(clan1)
                                    if clan2 not in kopiraj_u_isto:
                                        kopiraj_u_isto.append(clan2)
                                else:
                                    if clan1 not in kopiraj_u_isto:
                                        kopiraj_u_isto.append(clan1)
                                    if clan2 not in kopiraj_u_razlicito:
                                        kopiraj_u_razlicito.append(clan2)

                                usporedba.append(kopiraj_u_isto)
                                usporedba.append(kopiraj_u_razlicito)

                            if len(skup_simbola_abecede)>1:
                                for h in usporedba:
                                    if len(h) == 1:
                                        isti = False
                                        break
                            else:
                                if (len(usporedba[0]) == 2) or (len(usporedba[1]) == 2):
                                    isti = True
                                else:
                                    isti = False

                        if isti==True:
                            if clan1 not in pomocna1:
                                if clan1 not in pomocna2:   # dodana linija
                                    pomocna1.append(clan1)
                            if clan2 not in pomocna1:
                                if clan2 not in pomocna2:   # dodana linija
                                    pomocna1.append(clan2)
                        else:
                            if clan1 not in pomocna1:
                                if clan1 not in pomocna2:   # dodana linija
                                    pomocna1.append(clan1)
                            if clan2 not in pomocna2:
                                if clan2 not in pomocna1:
                                    pomocna2.append(clan2)
                        
            pomocna1.clear()
            for element in grupa:
                if element in pomocna2:
                    continue
                else:
                    pomocna1.append(element)

            if len(pomocna1) > 0 and len(pomocna2) > 0:
                nove_grupe.remove(grupa)
                nove_grupe.append(pomocna1)
                nove_grupe.append(pomocna2)

    grupe = nove_grupe
    izlazimo = len(grupe)

    if izlaz == izlazimo:
        break

grupe.sort()
min_dka_stanja = []

dfs(pocetno_stanje)

for grupa in grupe:
    if len(grupa) > 0:
        for clan in grupa:
            if clan in dohvatljiva_stanja:
                min_dka_stanja.append(clan)
                break

ispis = (",").join(min_dka_stanja)
print(ispis)
ispis_prijelaza = (",").join(skup_simbola_abecede)
print(ispis_prijelaza)

nova_prihvatljiva = []
for clan in skup_prihvatljivih_stanja:
    if clan in min_dka_stanja:
        nova_prihvatljiva.append(clan)

if len(skup_prihvatljivih_stanja) > 0:
    ispis_prihvatljivih = (",").join(nova_prihvatljiva)
    print(ispis_prihvatljivih)
else:
    print()

if pocetno_stanje not in min_dka_stanja:
    for grupa in grupe:
        if pocetno_stanje in grupa:
            pocetno_stanje = grupa[0]
print(pocetno_stanje)

for kljuc in prijelaz:
    key = kljuc.split(",")
    stanje_kljuca = key[0]
    if stanje_kljuca in min_dka_stanja:
        value = prijelaz[kljuc]
        if value in min_dka_stanja:
            ispisi = stanje_kljuca + "," + key[1] + "->" + value
            print(ispisi)
        else:
            for grupa in grupe:
                if value in grupa:
                    value = grupa[0]
            ispisi = stanje_kljuca + "," + key[1] + "->" + value
            print(ispisi) 