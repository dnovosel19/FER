#include <iostream>
#include <cstdlib>

using namespace std;

void matrixx(int n, int k, int polje[], int** matrica){
    for(int i=0; i<n; i++) {
        for(int j=0; j<n; j++) {
            if((i!=j) && (abs(polje[i] - polje[j]) == k)) {
                matrica[i][j] = 1;
            }
        }
    }
}

void obilazak(int u, bool vidi[], int** matrica, int n) {
   vidi[u] = true;
   for(int i=0; i<n; i++) {
      if(matrica[u][i]) {
         if(!vidi[i])
            obilazak(i, vidi, matrica, n);
      }
   }
}

bool jePovezan(int** polje, int n) {
    bool *vidi = new bool[n];
    for(int i=0; i<n; i++) {
        for(int j=0; j<n; j++) {
            vidi[j] = false;
        }
        obilazak(i, vidi, polje, n);
        for(int j=0; j<n; j++) {
            if(!vidi[j]) {
                return false;
            }
        }
    }
    return true;
}

bool daMoze(int i, int** matrica, int put[], int pozicija) {
    if(matrica[put[pozicija-1]][i] == 0)
        return false;
    for(int j=0; j<pozicija; j++) {
        if(put[j] == i)
            return false;
    }
    return true;
}

bool hamCiklus(int** matrica, int put[], int pozicija, int n) {
    if(n <= 2) return false;
    if(pozicija == n) {
        if(matrica[put[pozicija-1]][put[0]] == 1)
            return true;
        else
            return false;
    }

    for(int i=1; i<n; i++) {
        if(daMoze(i, matrica, put, pozicija)) {
            put[pozicija] = i;
            if(hamCiklus(matrica, put, pozicija+1, n) == true) {
                return true;
            }
            put[pozicija] = -1;
        }
    }
    return false;
}

void jeHamilton(int** matrica, int n) {
    int *put = new int[n];
    for(int i=0; i<n; i++) {
        put[i] = -1;
    }
    put[0] = 0;

    if(hamCiklus(matrica, put, 1, n) == false) {
        cout << "Graf G nije hamiltonovski graf";
    } else {
        cout << "Graf G je hamiltonovski graf";
    }
}

int main() {
    int n;
    cout << "Unesite prirodan broj n: ";
    cin >> n;

    int k1, k2, k3, k4;
    cout << "Unesite vrijednost prirodnog broja k_1: ";
    cin >> k1;
    cout << "Unesite vrijednost prirodnog broja k_2: ";
    cin >> k2;
    cout << "Unesite vrijednost prirodnog broja k_3: ";
    cin >> k3;
    cout << "Unesite vrijednost prirodnog broja k_4: ";
    cin >> k4;

    int *polje = new int[n];
    //cout << "Polje: ";
    for(int i=0; i<n; i++) {
        polje[i] = i+1;
        //cout << polje[i] << " ";
    }
    cout << endl;

    int **matrica = new int*[n];
    for(int i=0; i<n; i++) {
        matrica[i] = new int[n];
        for(int j=0; j<n; j++) {
            matrica[i][j] = 0;
        }
    }

    matrixx(n, k1, polje, matrica);
    matrixx(n, k2, polje, matrica);
    matrixx(n, k3, polje, matrica);
    matrixx(n, k4, polje, matrica);


    /*for(int i=0; i<n; i++) {
        for(int j=0; j<n; j++) {
            cout << matrica[i][j] << " ";
        }
        cout << endl;
    }*/

    if(jePovezan(matrica, n)) {
        cout << "Graf G je povezan graf" << endl;
        jeHamilton(matrica, n);
    } else {
        cout << "Graf G nije povezan graf" << endl;
        cout << "Graf G nije hamiltonovski graf";
    }

    return 0;
}