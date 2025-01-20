import sys

polje_redaka = []
for line in sys.stdin:
    polje_redaka.append(line)

def ima_slova(varijabla):
    novo = list(varijabla)
    for i in novo:
        if i.isalpha():
            return True
    return False

def odredi_naziv(naziv):
    if naziv == "=":
        ispis = "OP_PRIDRUZI " + broj_red + " ="
        #print("OP_PRIDRUZI " + broj_red + " =")
    elif naziv == "+":
        ispis = "OP_PLUS " + broj_red + " +"
        #print("OP_PLUS " + broj_red + " +")
    elif naziv == "-":
        ispis = "OP_MINUS " + broj_red + " -"
        #print("OP_MINUS " + broj_red + " -")
    elif naziv == "*":
        ispis = "OP_PUTA " + broj_red + " *"
        #print("OP_PUTA " + broj_red + " *")
    elif naziv == "/":
        ispis = "OP_DIJELI " + broj_red + " /"
        #print("OP_DIJELI " + broj_red + " /")
    elif naziv == "(":
        ispis = "L_ZAGRADA " + broj_red + " ("
        #print("L_ZAGRADA " + broj_red + " (")
    elif naziv == ")":
        ispis = "D_ZAGRADA " + broj_red + " )"
        #print("D_ZAGRADA " + broj_red + " )")
    elif naziv == "za":
        ispis = "KR_ZA " + broj_red + " za"
        #print("KR_ZA " + broj_red + " za")
    elif naziv == "od":
        ispis = "KR_OD " + broj_red + " od"
        #print("KR_OD " + broj_red + " od")
    elif naziv == "do":
        ispis = "KR_DO " + broj_red + " do"
        #print("KR_DO " + broj_red + " do")
    elif naziv == "az":
        ispis = "KR_AZ " + broj_red + " az"
        #print("KR_AZ " + broj_red + " az")
    elif naziv.isnumeric() == True:
        ispis = "BROJ " + broj_red + " " + naziv
        #print("BROJ " + broj_red + " " + naziv)
    else:
        ispis = "IDN " + broj_red + " " + naziv
        #print("IDN " + broj_red + " " + naziv)

    print(ispis.strip())

#citaj_file = open("ppj.txt", "r")
#polje_redaka = citaj_file.readlines()

broj_redak = 0
zastavica = 0

for i in polje_redaka:
    broj_redak = broj_redak + 1
    broj_red = str(broj_redak)
    redak_odvojen_razmakom = []
    redak_odvojen_razmakom = i.strip().split(" ")

    for j in redak_odvojen_razmakom:
        if len(j) >= 2:
            if j[0] == "/" and j[1] == "/":
                break
        if zastavica == 1:
            zastavica = 0
            break
        if j == "" or j == "\t":
            continue
        if j == "//":
            break
        else:
            niz = list(j)
            lista = ""

            for k in range(0, len(niz)):
                if niz[k] == "=" or niz[k] == "+" or niz[k] == "-" or niz[k] == "*" or niz[k] == "/" or niz[k] == "(" or niz[k] == ")" or niz[k] == "za" or niz[k] == "az" or niz[k] == "od" or niz[k] == "do":
                    odredi_naziv(niz[k])
                elif niz[k] == "" or niz[k] == "\t":
                    continue
                else:
                    lista += niz[k]
                    if k < len(niz)-1:
                        if lista.isnumeric() and niz[k+1].isalpha():
                            odredi_naziv(lista)
                            lista = ""
                            continue

                        if niz[k] == "/" and niz[k+1] == "/":
                            zastavica = 1
                            break

                        if niz[k].isnumeric() and niz[k+1].isnumeric():
                            continue
                        elif niz[k].isalpha() and (niz[k+1].isnumeric() or niz[k+1].isalpha()):
                            continue
                        else:
                            odredi_naziv(lista)
                            lista = ""
                            continue
                    if lista != "":
                        odredi_naziv(lista)
                        lista = ""