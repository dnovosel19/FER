import sys

arr = []
for line in sys.stdin:
    arr.append(line)

niz = []
niz = arr[0].strip()
niz_charova = []
for i in niz:
    niz_charova.append(i)
niz_charova.append('')

polje = []
polje.append("S")
brojac_znakova = 0
brojac_nezavrsnih = 0

pamti = []
da_ne = 1
broj_za_pamcenje = 0
stogic = []
stog_brojac = -1
smijes = []
smijes_brojac = -1

while True:
    if len(pamti) != 0 and (brojac_nezavrsnih >= len(polje)):
        polje.append(pamti[0])
        pamti.pop(0)
        if stog_brojac != -1:
            if stogic[stog_brojac] != 1:
                stogic[stog_brojac] = stogic[stog_brojac] - 1
                if stogic[stog_brojac] == 1:
                    stogic.pop(stog_brojac)
                    stog_brojac = stog_brojac - 1
                    smijes[smijes_brojac] = 1

    if brojac_znakova + 3 <= len(niz_charova):
        if niz_charova[brojac_znakova] == 'b' and niz_charova[brojac_znakova + 1] == 'c' and niz_charova[brojac_znakova + 2] != 'c' and broj_za_pamcenje != 0 and polje[-1] != "":
            if smijes[-1] == 1:
                smijes.pop(stog_brojac+1)
                smijes_brojac = smijes_brojac-1
                brojac_znakova = brojac_znakova + 2
                broj_za_pamcenje = broj_za_pamcenje - 1
                continue
    
    if brojac_znakova == len(niz_charova) and polje[-1] != "C":
        break
    elif brojac_znakova > len(niz_charova):
        da_ne = 0
        break

    if brojac_nezavrsnih >= len(polje):
        if brojac_nezavrsnih == len(polje):
            if brojac_znakova + 2 == len(niz_charova):
                if niz_charova[-2] == 'b' and niz_charova[-1] == 'c':
                    break
        if brojac_znakova+2 < len(niz_charova):
            da_ne = 0
            break
        da_ne = 1
        break

    if polje[brojac_nezavrsnih] == 'S':
        if niz_charova[brojac_znakova] == 'a':
            if stog_brojac != -1:
                stogic[stog_brojac] = stogic[stog_brojac] + 1
            polje.append("A")
            pamti.insert(0, "B")
        elif niz_charova[brojac_znakova] == 'b':
            if stog_brojac != -1:
                stogic[stog_brojac] = stogic[stog_brojac] + 1
            polje.append("B")
            pamti.insert(0, "A")
        else:
            da_ne = 0
            break
        brojac_znakova = brojac_znakova + 1
        brojac_nezavrsnih = brojac_nezavrsnih + 1

    elif polje[brojac_nezavrsnih] == 'A':
        if niz_charova[brojac_znakova] == 'a':
            brojac_znakova = brojac_znakova
        elif niz_charova[brojac_znakova] == 'b':
            polje.append("C")
        else:
            da_ne = 0
            break
        brojac_nezavrsnih = brojac_nezavrsnih + 1
        brojac_znakova = brojac_znakova + 1

    elif polje[brojac_nezavrsnih] == 'B':
        if brojac_znakova + 1 <= len(niz_charova):
            if niz_charova[brojac_znakova] == 'c' and niz_charova[brojac_znakova + 1] == 'c':
                polje.append("S")
                broj_za_pamcenje = broj_za_pamcenje + 1
                brojac_znakova = brojac_znakova + 2
                smijes.append(0)
                stogic.append(0)    #broji kolko ih je na stogu, svaki rekurzivno
                stog_brojac = stog_brojac + 1   #prati koji je indeks zadnji
                smijes_brojac = smijes_brojac + 1
                stogic[stog_brojac] = stogic[stog_brojac] + 1 #reci da je 1 kao postoji nekaj za stog
            elif niz_charova[brojac_znakova] == '':
                da_ne = 1
                break
        brojac_nezavrsnih = brojac_nezavrsnih + 1

    else:
        polje.append("A")
        pamti.insert(0, "A")
        if stog_brojac != -1:
            stogic[stog_brojac] = stogic[stog_brojac] + 1
        brojac_nezavrsnih = brojac_nezavrsnih + 1


ispis = ''
for i in polje:
    ispis += i

print(ispis)
if da_ne == 1 and len(pamti) == 0:
    print("DA")
else:
   print("NE")