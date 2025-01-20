#! /bin/sh
#
# Dodajte ili modificirajte pravila na oznacenim mjestima ili po potrebi (i želji) na 
# nekom drugom odgovarajucem mjestu (pazite: pravila se obrađuju slijedno!)
#
IPT=/sbin/iptables

$IPT -P INPUT DROP
$IPT -P OUTPUT DROP
$IPT -P FORWARD DROP

$IPT -F INPUT
$IPT -F OUTPUT
$IPT -F FORWARD

$IPT -A INPUT   -m state --state ESTABLISHED,RELATED -j ACCEPT
$IPT -A OUTPUT  -m state --state ESTABLISHED,RELATED -j ACCEPT
$IPT -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT

#
# za potrebe testiranja dozvoljen je ICMP (ping i sve ostalo)
#
$IPT -A INPUT   -p icmp -j ACCEPT
$IPT -A FORWARD -p icmp -j ACCEPT
$IPT -A OUTPUT  -p icmp -j ACCEPT

#
# Primjer "anti spoofing" pravila na sucelju eth0
#
#$IPT -A INPUT   -i eth0 -s 127.0.0.0/8  -j DROP
#$IPT -A FORWARD -i eth0 -s 127.0.0.0/8  -j DROP
#$IPT -A INPUT   -i eth0 -s 203.0.113.0/24  -j DROP
#$IPT -A FORWARD -i eth0 -s 203.0.113.0/24  -j DROP
#$IPT -A INPUT   -i eth0 -s 10.0.0.0/24  -j DROP
#$IPT -A FORWARD -i eth0 -s 10.0.0.0/24  -j DROP
#$IPT -A INPUT   -i eth0 -s 192.168.1.2  -j DROP
#$IPT -A FORWARD -i eth0 -s 192.168.1.2  -j DROP

#
# Web poslužitelju (tcp/80 i tcp/443) pokrenutom na www se može 
# pristupiti s bilo koje adrese (iz Interneta i iz lokalne mreže), ...
#
$IPT -A INPUT -p tcp --dport 80 -j ACCEPT
$IPT -A INPUT -p tcp --dport 443 -j ACCEPT

#
# DNS poslužitelju (udp/53 i tcp/53) pokrenutom na www se može 
# pristupiti s bilo koje adrese (iz Interneta i iz lokalne mreže), ...
#
$IPT -A INPUT -p udp --dport 53 -j ACCEPT
$IPT -A INPUT -p tcp --dport 53 -j ACCEPT

#
# ... a SSH poslužitelju na www samo s racunala admin iz lokalne mreže "Private"
# 
$IPT -A INPUT -p tcp -s 10.0.0.20 --dport 22 -j ACCEPT

#
# ... kao i SSH poslužitelju na dns (samo s racunala admin iz lokalne mreže "Private")
# 
$IPT -A INPUT -p tcp -s 10.0.0.20 --dport 22 -j ACCEPT

# 
# S www je dozvoljen pristup poslužitelju database (Private) na TCP portu 10000 te pristup 
# DNS poslužiteljima u Internetu (UDP i TCP port 53).
#
$IPT -A OUTPUT -p tcp -d 10.0.0.100 --dport 10000 -j ACCEPT
$IPT -A OUTPUT -p udp --dport 53 -j ACCEPT
$IPT -A OUTPUT -p tcp --dport 53 -j ACCEPT

#
# ... S www je zabranjen pristup svim ostalim adresama i poslužiteljima.
#
$IPT -A OUTPUT -j REJECT

#
#
# Pristup svim ostalim adresama i poslužiteljima u DMZ je zabranjen.
#
$IPT -A FORWARD -j REJECT

#
# Pristup SSH poslužitelju na cvoru database, koji se nalazi u lokalnoj mreži "Private", 
# dozvoljen je samo racunalima iz mreže "Private".
#
$IPT -A INPUT -p tcp -s 10.0.0.0/24 --dport 22 -j ACCEPT

#
# Web poslužitelju na cvoru database, koji sluša na TCP portu 10000, može se pristupiti
# iskljucivo s racunala www koje se nalazi u DMZ (i s racunala iz mreže "Private").
#
$IPT -A INPUT -p tcp -s 203.0.113.0/24 --dport 10000 -j ACCEPT
$IPT -A INPUT -p tcp -s 10.0.0.0/24 --dport 10000 -j ACCEPT

#
# S racunala database je zabranjen pristup svim uslugama u Internetu i u DMZ.
#
$IPT -A FORWARD -d 10.0.0.100 -j REJECT

# Zabranjen je pristup svim ostalim uslugama na poslužitelju database (iz Interneta i iz DMZ)
#
$IPT -A FORWARD -d 10.0.0.100 -j REJECT

#
# S racunala iz lokalne mreže "Private" (osim s database) se može pristupati svim racunalima 
# u Internetu ali samo korištenjem protokola HTTP (tcp/80 i tcp/443) i DNS (udp/53 i tcp/53).
#
$IPT -A FORWARD -p tcp -s 10.0.0.0/24 -d ! 10.0.0.100 --dport 80 -j ACCEPT
$IPT -A FORWARD -p udp -s 10.0.0.0/24 --dport 53 -j ACCEPT
$IPT -A FORWARD -p tcp -s 10.0.0.0/24 --dport 53 -j ACCEPT

#
# Pristup iz vanjske mreže u lokalnu LAN mrežu je zabranjen.
#
$IPT -A FORWARD -s 0.0.0.0/0 -d 10.0.0.0/24 -j REJECT

#
# Na FW je pokrenut SSH poslužitelj kojem se može pristupiti samo iz lokalne mreže "Private"
# i to samo sa cvora admin.
#
$IPT -A INPUT -p tcp -s 10.0.0.2 --dport 22 -j ACCEPT

#
# Pristup svim ostalim uslugama (portovima) na cvoru FW je zabranjen.
#
$IPT -A INPUT -j REJECT

