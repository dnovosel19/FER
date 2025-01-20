import sys
import getpass
import bcrypt

# provjera sadrzi li lozinka malo i veliko slovo, barem jedan broj, neki poseban znak te duljinu barem 8 znakova
def provjera_ispravnosti_lozinke(lozinka):
    veliko = False
    malo = False
    broj = False
    poseban_znak = False
    if len(lozinka) < 8:
        duljina = False
    else:
        duljina = True

    for i in lozinka:
        if i.isdigit():
            broj = True
        if i.isupper():
            veliko = True
        if i.islower():
            malo = True
        if not i.isalnum():
            poseban_znak = True
    return veliko and malo and broj and poseban_znak and duljina

# dodaj novog korisnika u bazu
def add(korisnicko_ime):

    # provjera postoji li vec neki user istog korisnickog imena
    with open("userbase.txt", "r") as file:
        users = file.readlines()
    for i in users:
        user = i.split()
        if user[0] == korisnicko_ime:
            print("Cannot add a new user with the same username.")
            exit()
    password = getpass.getpass(prompt="Password:")

    # provjera zadovoljava li password sve uvjete da bude dovoljno jak
    while True:
        if provjera_ispravnosti_lozinke(password):
            break
        else:
            print("Password isn't strong enough.")
            password = getpass.getpass(prompt="Password:")
    
    repeat_password = getpass.getpass(prompt="Repeat Password:")
    
    # hashiranje lozinke i zapisivanje u bazu
    if password == repeat_password:
        # hashiranje passworda i zapis u datoteku
        salt = bcrypt.gensalt()
        bytes_password = password.encode('utf-8')
        hash = bcrypt.hashpw(bytes_password, salt)
        zapisi = ''
        zapisi += korisnicko_ime + ' ' + salt.decode() + ' ' + hash.decode() + ' 0\n'
        with open("userbase.txt" , "a") as file:
            file.write(zapisi)
        print("User " + korisnicko_ime + " successfily added.")
    
    else:
        print("User add failed. Password mismatch.")

# promjeni lozinku
def passwd(korisnicko_ime):
    with open("userbase.txt", "r") as file:
        users = file.readlines()

    password = getpass.getpass(prompt="Password:")
    user_postoji = 0

    # trazenje korisnickog imena kako bi se password promijenio
    for ind, i in enumerate(users):
        user = i.split()
        if user[0] == korisnicko_ime:
            user_postoji = 1
            salt = user[1].encode()

            # provjera lozinke
            while True:
                bytes_password = password.encode('utf-8')
                hash = bcrypt.hashpw(bytes_password, salt)
                if provjera_ispravnosti_lozinke(password):
                    if hash.decode() == user[2]:
                        print("Cannot change the password to the same password")
                        password = getpass.getpass(prompt="Password:")
                    else:
                        break
                else:
                    print("Password isn't strong enough.")
                    password = getpass.getpass(prompt="Password:")
    
    # ako ne postoji taj username
    if user_postoji == 0:
        print("User doesn't exist")
        exit()
    
    repeat_password = getpass.getpass(prompt="Repeat Password:")

    if password == repeat_password:
        salt = bcrypt.gensalt()
        bytes_password = password.encode('utf-8')
        hash = bcrypt.hashpw(bytes_password, salt)

        novi_zapis = ''
        novi_zapis += korisnicko_ime + ' ' + salt.decode() + ' ' + hash.decode()

        pronaden = 0
        zapisi = ''
        for ind, i in enumerate(users):
            user = i.split()
            if user[0] == korisnicko_ime:
                zapisi += novi_zapis + ' ' + user[3] + '\n'
                pronaden = 1
            else:
                zapisi += users[ind]
        
        if pronaden:
            with open("userbase.txt", "w") as file:
                file.write(zapisi)
            print("Password change successful.")
        else:
            print("User doesn't exist")

    else:
        print("Password change failed. Password mismatch.")

# zahtjevaj promjenu lozinke 
def forcepass(korisnicko_ime):

    with open("userbase.txt", "r") as file:
        users = file.readlines()

    # pronadi tog usera i u bazi podataka zapisi zastavicu koja signalizira da se mora promijenit password
    zapisi = ''
    postoji = 0
    for ind, i in enumerate(users):
        user = i.split()
        if user[0] == korisnicko_ime:
            zapisi += user[0] + ' ' + user[1] + ' ' + user[2] + ' 1\n'
            postoji = 1
        else:
            zapisi += users[ind]
        
    if postoji:
        with open("userbase.txt", "w") as file:
            file.write(zapisi)
        print("User will be requested to change password on next login.")
    else:
        print("User doesn't exist")

# izbrisi usera
def delete(korisnicko_ime):
    with open("userbase.txt", "r") as file:
        users = file.readlines()
    
    # pronadi ga i ignoriraj ga
    zapisi = ''
    postoji = 0
    for ind, i in enumerate(users):
        user = i.split()
        if user[0] == korisnicko_ime:
            postoji = 1
            continue
        else:
            zapisi += users[ind]
    
    if postoji:
        with open("userbase.txt", "w") as file:
            file.write(zapisi)
        print("User successfuly removed.")
    else:
        print("User doesn't exist")

unos = sys.argv
command = unos[1]

if command == "add":
    add(unos[2])
elif command == "passwd":
    passwd(unos[2])
elif command == "forcepass":
    forcepass(unos[2])
elif command == "del":
    delete(unos[2])