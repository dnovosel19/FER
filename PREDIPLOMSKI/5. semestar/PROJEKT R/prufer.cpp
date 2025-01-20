#include<iostream>
using namespace std;

void kodPrufer(int **stablo, int n) {
    int static stani = 0;   // varijabla koju koristimo za ispis zareza
    int cvor[n] = {0};      // polje od n clanova, svi na pocetku 0

    for(int i=0; i<n; i++) {    // po redovima broji koliko ima poveznica, jedinica
        for(int j=0; j<n; j++) { // sa koliko je vrhova povezan trenutni vrh
            if(stablo[i][j])
                cvor[i]++;
        }
    }

    for(int k=0; k<n; k++) {
        if(cvor[k] >= 2) {  // ako postoji vrh koji nije list, bitno samo pri prvom ulasku u funkciju
            for(int i=0; i<n; i++) {
                if(cvor[i] == 1) {  // pronalazimo list
                    for(int j=0; j<n; j++) {
                        if(stablo[i][j] == 1) { // pronalazimo sa kojim je vrhom list spojen
                            cout << j+1;    // ispis
                            stani++;
                            if(stani != (n-2)) {
                                cout << ", ";
                            }
                        }
                        stablo[i][j] = 0; // 'brisanje' vrhova
                        stablo[j][i] = 0;
                    }
                    break;
                }
            }
            break;
        }
    }

    for(int i=0; i<n; i++) {
        if(cvor[i] >= 2) {  // ako postoji jos vrhova koji nisu listovi, onda nastavi
            kodPrufer(stablo, n);
        }
    }
    return;
}

int main() {
    int n;  // matrica n*n
    cout << "Unesite prirodan broj n: ";
    cin >> n;

    int **matrica = new int*[n];    // stvaranje matrice, svi elementi su 0
    for(int i=0; i<n; i++) {
        matrica[i] = new int[n];
        for(int j=0; j<n; j++) {
            matrica[i][j] = 0;
        }
    }

    for(int i=1; i<n; i++) {       // kreiranje stabla, pretpostavka da je stablo dobro uneseno (da graf zaista jest stablo)
        for(int j=i+1; j<=n; j++) {
            int k;
            cout << "Unesi 1 ako su bridovi " << i << " i " << j << " povezani, inace unesi 0: ";
            cin >> k;
            if(k != 0) {
                matrica[i-1][j-1] = k;
                matrica[j-1][i-1] = k;
            }
        }
    }

    for(int i=0; i<n; i++) {    // izgled grafa
        for(int j=0; j<n; j++) {
            cout << matrica[i][j] << " ";
        }
        cout << endl;
    }

    // Pruferov kod se ispisuje dobro akko je stablo pravilno upisano
    cout << "Pruferov kod vaseg grafa jest: ("; // ispis Pruferovog koda
    kodPrufer(matrica, n);
    cout << ")";
}