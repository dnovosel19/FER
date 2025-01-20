#include<iostream>
#include<bits/stdc++.h>
using namespace std;


void obilazak(int u, bool vidi[], int** matrica, int n) {
   vidi[u] = true;
   for(int i=0; i<n; i++) {
      if(matrica[u][i] != 0) {
         if(!vidi[i])
            obilazak(i, vidi, matrica, n);
      }
   }
}

bool jePovezan(int** polje, int n) {    // provjera povezanosti grafa
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

void kodPrufer(int **stablo, int n, int polje[]) {  // u polje zapisujemo Pruferov kod
    int static stani = 0;   // varijabla koju koristimo za ispis zareza
    int cvor[n] = {0};      // polje od n clanova, svi na pocetku 0

    for(int i=0; i<n; i++) {    // po redovima broji koliko ima poveznica, jedinica
        for(int j=0; j<n; j++) { // sa koliko je vrhova povezan trenutni vrh
            if(stablo[i][j])
                cvor[i]++;
        }
    }

    int static brojac = 0;  // pomicanje u polju, zapisi brojeve Pruferovog koda
    for(int k=0; k<n; k++) {
        if(cvor[k] >= 2) {  // treba postojati vrh koji nije list, bitno samo pri prvom ulasku u funkciju
            for(int i=0; i<n; i++) {
                if(cvor[i] == 1) {  // pronalazimo list
                    for(int j=0; j<n; j++) {
                        if(stablo[i][j] == 1) { // pronalazimo sa kojim je vrhom list spojen
                            cout << j+1;    // ispis
                            polje[brojac] = j + 1;
                            brojac++;
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
            kodPrufer(stablo, n, polje);
        }
    }
    return;
}

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
            if(zastavica == 0)                      // ako smo ga vec prije pronasli onda ga zanemarujemo i nastavljamo dalje
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

struct Skup {   // koristimo samo zbog funkcija find i merge
    int *parent, *rank;
    int n;
  
    Skup(int n) {   // konstruktor
        this->n = n;
        parent = new int[n+1];
        rank = new int[n+1];
  
        for (int i = 0; i <= n; i++) {
            rank[i] = 0;
            parent[i] = i;  // sam sebi je roditelj
        }
    }
  
    int find(int u) {   // nadi roditelja cvora u
        if (u != parent[u])
            parent[u] = find(parent[u]);
        return parent[u];
    }
  
    void merge(int x, int y) {  // unija
        x = find(x), y = find(y);
  
        if (rank[x] > rank[y])
            parent[y] = x;
        else
            parent[x] = y;
  
        if (rank[x] == rank[y])
            rank[y]++;
    }
};
  
struct Graph {
    int V, E;   // V (vertex) vrhovi, E (edge) bridovi
    vector< pair<int, pair<int, int>> > edges;
  
    Graph(int V, int E) {   // kostruktor
        this->V = V;
        this->E = E;
    }

    void addEdge(int u, int v, int w) { // dodavanje bridova
        edges.push_back({w, {u, v}});
    }
    
    int kruskal(int pomm, int pomocc[]) {   // kruskalov algoritam
        int tmrs = 0;   // tezina minimalno razapinjuceg stabla

        sort(edges.begin(), edges.end());   // rastuce sortiraj bridove
        Skup ds(V);

        vector< pair<int, pair<int, int>> >::iterator it;   // omogucava nam iteraciju po bridovima
        for (it=edges.begin(); it!=edges.end(); it++) {
            int u = it->second.first;
            int v = it->second.second;

            int set_u = ds.find(u); // brid
            int set_v = ds.find(v); // brid

            if (set_u != set_v) {   // provjera cine li ciklus
                pomocc[pomm++] = u;
                pomocc[pomm++] = v;

                tmrs += it->first;

                ds.merge(set_u, set_v);
            }
        }

        return tmrs;
    }
};  
  
int main() {
    int n, a, b, c;
    cout << "Unesite prirodan broj n: ";
    cin >> n;
    cout << "Unesite prirodan broj a: ";
    cin >> a;
    cout << "Unesite prirodan broj b: ";
    cin >> b;
    cout << "Unesite prirodan broj c: ";
    cin >> c;

    int **matrica = new int*[n];    // kreiraj matricu
    for(int i=0; i<n; i++) {
        matrica[i] = new int[n];
        for(int j=0; j<n; j++) {
            matrica[i][j] = 0;
        }
    }

    int bridovi = 0;
    for(int i=1; i<n; i++) {
        for(int j=i+1; j<=n; j++) {
            int k = abs(a*i - b*j) / c; // neka funkcija za upisivanje brojeva u matricu
            if(k != 0) {
                bridovi++;
                matrica[i-1][j-1] = k;  // mora biti simetricna matrica, zato su uvijek vrijednosti
                matrica[j-1][i-1] = k;  // na (i,j) jednake kao i na (j,i)
            }
        }
    }

    if(jePovezan(matrica, n)) { // ima smisla gledati samo ako je graf povezan 
        cout << "Graf G je povezan graf" << endl;

        int V = n, E = bridovi;
        Graph g(V, E);

        int **stablo = new int*[n]; // priprema za kreiranje stabla
        for(int i=0; i<n; i++) {
            stablo[i] = new int[n];
            for(int j=0; j<n; j++) {
                stablo[i][j] = 0;
            }
        }

        for(int i=0; i<V-1; i++) {  // dodajemo bridove matrici
            for(int j=i+1; j<V; j++) {
                if(matrica[i][j] != 0) {
                    g.addEdge(i, j, matrica[i][j]);
                }
            }
        }

        int pom = 0;
        int pomoc[n*(n-1)]; // dovoljno elemenata zato sto ignoriramo dijagonalu (pretpostavljamo da nema petlji)
        for(int i=0; i<n*(n-1); i++) {
            pomoc[i] = 0;
        }
  
        int tmrs = g.kruskal(pom, pomoc);   // kruskalovim algoritmom pamtimo na koje mjesto moramo staviti 1 da dobijemo stablo

        for(int i=0; i<n*(n-1); i=i+2) {    // krecemo se po dva jer u polju su svaka dva "par", odnosno predstavljaju koja dva vrha su spojena
            stablo[pomoc[i]][pomoc[i+1]] = 1;   // simetricna matrica
            stablo[pomoc[i+1]][pomoc[i]] = 1;
            // cout << pomoc[i] << " " << pomoc[i+1] << endl;
        }
        stablo[0][0] = 0;   // samo zanemarujemo kada dobijemo 

        cout << "Minimalno razapinjuce stablo:" << endl;   // ispis dobivenog stabla
        for(int i=0; i<n; i++) {
            for(int j=0; j<n; j++) {
                cout << stablo[i][j] << " ";
            }
        cout << endl;
        }

        int polje[n];   // polje za pamtiti Prufera
        for(int i=0; i<n; i++) {
            polje[i] = 0;
        }
        cout << "Pruferov kod vaseg grafa jest: ("; // ispis Pruferovog koda
        kodPrufer(stablo, n, polje);
        cout << ")" << endl;

        obrnutiPrufer(polje, n-2);

        // cout << "Ukupna tezina minimalnog razapinjuceg stabla:  " << tmrs;

    } else {
        cout << "Graf G nije povezan graf" << endl;
    }

    return 0;
}