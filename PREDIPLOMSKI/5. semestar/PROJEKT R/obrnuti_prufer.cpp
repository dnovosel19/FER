#include <iostream>

using namespace std;

void obrnutiPrufer(int pruf_kod[], int duljina) {
    // matrica koja u prvom redu pamti b1, a u drugom brojeve Pruferovog koda
    int **bridovi = new int*[duljina+1];
    for(int i=0; i<2; i++) {
        bridovi[i] = new int[duljina+1];
        for(int j=0; j<duljina+1; j++) {
            bridovi[i][j] = 0;
        }
    }

    int brojac = 0, nemoj_preskociti = 1;           // brojac pamti koje smo brojeve Pruferova koda obradili, a nemoj_preskociti = 1 govori je li taj broj koji nam treba

    while(1) {
        for(int i=1; i<=duljina+2; i++) {
            nemoj_preskociti = 1;                   // mora se 'resetirati' provjera

            int zastavica = 1;                      // provjera jesmo li taj broj vec prije pronasli i zapisali
            for(int j=0; j<duljina; j++) {
                if(i == bridovi[0][j]) {
                    zastavica = 0;
                    break;
                }
            }
            if(zastavica == 0)                      // ako smo ga vec prije pronasli onda ga zanemarujemo i nastavljmao dalje
                continue;

            for(int j=brojac; j<duljina; j++) {     // trazimo po Pruferovom kodu
                if (i == pruf_kod[j]) {
                    nemoj_preskociti = 0;
                    break;
                }
            }
            if(nemoj_preskociti) {                  // ukoliko je broj dobar zapisujemo ga u prvi redak matrice na prvo mjesto gdje se nalazi 0
                bridovi[0][brojac] = i;
                bridovi[1][brojac] = pruf_kod[brojac];
                brojac++;
                break;
            }
        }

        if(bridovi[0][duljina-1] != 0) {            // uvjet kojim prekidamo beskonacnu petlju
            break;
        }
    }

    int pamti_prvi = 0, pamti_drugi = 0, necu = 0;  // pamti_prvi i pamti_drugi sluze da pronademo zadnji brid koji nam nedostaje
    for (int i=1; i<=duljina+2; i++) {
        necu = 0;                                   // necu provjerava je li trenutni broj onaj koji trazimo, ovdje ga 'resetiramo'
        for(int j=0; j<duljina+1; j++) {
            if(i == bridovi[0][j]) {                // ovim uvjetom znamo da nam taj broj ne treba
                necu = 1;
                break;
            }
        }
        if(necu == 0) {
            if(pamti_prvi == 0) {                   // prvi broj koji pronademo zapisemo u pamti_prvi
                pamti_prvi = i;
            } else {
                pamti_drugi = i;                    // drugi trazeni broj zapisujemo u pamti_drugi
                break;
            }
        }
    }
    if (duljina > 1) {                              // zapisujemo i zadnji brid u matricu
        bridovi[0][duljina] = pamti_prvi;
        bridovi[1][duljina] = pamti_drugi;
    }

    cout << "E(T) = {";                             // ispis bridova
    if(duljina > 1) {
        for(int j=0; j<duljina+1; j++) {
            if (bridovi[0][j] <= bridovi[1][j]) {
                cout << bridovi[0][j] << bridovi[1][j];
            } else {
                cout << bridovi[1][j] << bridovi[0][j];
            }
            if(j != duljina)
                cout << ", ";
        }
    } else {
        cout << bridovi[0][0] << bridovi[1][0];
    }
    cout << "}";
}

int main() {
    int n, a;
    
    // Unosimo broj sve dok nije ispravan
    do {
        cout << "Unesite nenegativan cijeli broj, od koliko se brojeva sastoji uredena n-torka Pruferovog koda: ";
        cin >> n;
    } while(n < 1);

    int *polje = new int[n];                        // polje u kojem pamtimo Pruferov kod kada ga unosimo

    for (int i=0; i<n; i++) {
        do {                                        // moraju biti ispravni brijevi
            cout << "Unesite " << i+1 << ". clan uredene " << n << "-torke, veci od 0: ";
            cin >> a;
        } while(a < 1);
        polje[i] = a;
    }

    // ispis Pruferovog koda
    cout << "Pruferov kod: (";
    for (int i=0; i<n; i++) {
        cout << polje[i];
        if (i < n-1) {
            cout << ", ";
        }
    }
    cout << ")" << endl;

    // funkcija za obrnuti Pruferov kod
    obrnutiPrufer(polje, n);
    
    return 0;
}