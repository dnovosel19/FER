#!/bin/bash

# inicijalizacije password managera baze podataka
echo "python .\srslab1.py init prvaSIfra"

# nova inicijalizacija baze
echo "python .\srslab1.py init mAsterPasswrd"

# pohrana lozinke za www.fer.hr
echo "python .\srslab1.py put mAsterPasswrd www.fer.hr neprobojnAsifrA"

# pohrana novog para adresa, lozinka
echo "python .\srslab1.py put mAsterPasswrd www.moodle.hr moodddllleee"

# promjena lozinke na adresi www.fer.hr
echo "python .\srslab1.py put mAsterPasswrd www.fer.hr drUGAcIjASIFra"

# pokusaj promjene lozinke uz krivi master password
echo "python .\srslab1.py put kriviMaster www.fer.hr neusPJEh"

# pokusaj dodavanja para adresa, lozinka, ali uz krivi master password
echo "python .\srslab1.py put MASTERpassword www.ferko.hr neSPrema"

# dohvacanje lozinke za www.fer.hr
echo "python .\srslab1.py get mAsterPasswrd www.fer.hr"

# dohvacanje lozinke za www.fer.hr s pogresnom glavnom lozinkom
echo "python .\srslab1.py get wrongPasswrd www.fer.hr"

# pokusaj dohvata nepostojece adrese, master password je dobar
echo "python .\srslab1.py get mAsterPasswrd www.nepostojim"