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

struct Skup {   // koristimo samo zbog funkcija find i merge
    int *parent, *rnk;
    int n;
  
    Skup(int n) {
        this->n = n;
        parent = new int[n+1];
        rnk = new int[n+1];
  
        for (int i = 0; i <= n; i++) {
            rnk[i] = 0;
            parent[i] = i;
        }
    }
  
    int find(int u) {   // nadi roditelja cvora u
        if (u != parent[u])
            parent[u] = find(parent[u]);
        return parent[u];
    }
  
    void merge(int x, int y) {
        x = find(x), y = find(y);
  
        if (rnk[x] > rnk[y])
            parent[y] = x;
        else
            parent[x] = y;
  
        if (rnk[x] == rnk[y])
            rnk[y]++;
    }
};
  
struct Graph {
    int V, E;   // V (vertex) vrhovi, E (edge) bridovi
    vector< pair<int, pair<int, int>> > edges;
  
    Graph(int V, int E) {
        this->V = V;
        this->E = E;
    }

    void addEdge(int u, int v, int w) {
        edges.push_back({w, {u, v}});
    }
    
    int kruskal(int pomm, int pomocc[]) {
        int tmrs = 0;   // tezina minimalno razapinjuceg stabla

        sort(edges.begin(), edges.end());   // rastuce sortiraj bridove
        Skup ds(V);

        vector< pair<int, pair<int, int>> >::iterator it;   // omogucava nam iteraciju po bridovima
        for (it=edges.begin(); it!=edges.end(); it++) {
            int u = it->second.first;
            int v = it->second.second;

            int set_u = ds.find(u);
            int set_v = ds.find(v);

            if (set_u != set_v) {
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

    int **matrica = new int*[n];
    for(int i=0; i<n; i++) {
        matrica[i] = new int[n];
        for(int j=0; j<n; j++) {
            matrica[i][j] = 0;
        }
    }

    int bridovi = 0;
    for(int i=1; i<n; i++) {
        for(int j=i+1; j<=n; j++) {
            int k = abs(a*i - b*j) / c;
            if(k != 0) {
                bridovi++;
                matrica[i-1][j-1] = k;
                matrica[j-1][i-1] = k;
            }
        }
    }

    if(jePovezan(matrica, n)) {
        cout << "Graf G je povezan graf" << endl;

        int V = n, E = bridovi;
        Graph g(V, E);

        int **stablo = new int*[n];
        for(int i=0; i<n; i++) {
            stablo[i] = new int[n];
            for(int j=0; j<n; j++) {
                stablo[i][j] = 0;
            }
        }

        for(int i=0; i<V-1; i++) {
            for(int j=i+1; j<V; j++) {
                if(matrica[i][j] != 0) {
                    g.addEdge(i, j, matrica[i][j]);
                }
            }
        }

        int pom = 0;
        int pomoc[n*(n-1)];
        for(int i=0; i<n*(n-1); i++) {
            pomoc[i] = 0;
        }
  
        int tmrs = g.kruskal(pom, pomoc);

        for(int i=0; i<n*(n-1); i=i+2) {
            stablo[pomoc[i]][pomoc[i+1]] = 1;
            stablo[pomoc[i+1]][pomoc[i]] = 1;
            // cout << pomoc[i] << " " << pomoc[i+1] << endl;
        }
        stablo[0][0] = 0;

        cout << "Minimalno razapinjuce stablo:" << endl;
        for(int i=0; i<n; i++) {
            for(int j=0; j<n; j++) {
                cout << stablo[i][j] << " ";
            }
            cout << endl;
        }

        // cout << "Ukupna tezina minimalnog razapinjuceg stabla:  " << tmrs;

    } else {
        cout << "Graf G nije povezan graf" << endl;
    }

    return 0;
}