#include<iostream>
#include<bits/stdc++.h>
using namespace std;

int pomoc[100000000];
int pom = 0;

void obilazak(int u, bool vidi[], int** matrica, int n) {
   vidi[u] = true;
   for(int i=0; i<n; i++) {
      if(matrica[u][i] != 0) {
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
  
typedef pair<int, int> iPair;
  
struct Graph {
    int V, E;
    vector< pair<int, iPair> > edges;
  
    Graph(int V, int E) {
        this->V = V;
        this->E = E;
    }
  
    void addEdge(int u, int v, int w) {
        edges.push_back({w, {u, v}});
    }
  
    int kruskalMST();
};
  
struct DisjointSets {
    int *parent, *rnk;
    int n;
  
    DisjointSets(int n) {
        this->n = n;
        parent = new int[n+1];
        rnk = new int[n+1];
  
        for (int i = 0; i <= n; i++) {
            rnk[i] = 0;
            parent[i] = i;
        }
    }
  
    int find(int u) {
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

  
int Graph::kruskalMST() {
    int mst_wt = 0;
  
    sort(edges.begin(), edges.end());
  
    DisjointSets ds(V);
  
    vector< pair<int, iPair> >::iterator it;
    for (it=edges.begin(); it!=edges.end(); it++) {
        int u = it->second.first;
        int v = it->second.second;
  
        int set_u = ds.find(u);
        int set_v = ds.find(v);
  
        if (set_u != set_v) {
            // cout << u << " - " << v << endl;
            pomoc[pom++] = u;
            pomoc[pom++] = v;
  
            mst_wt += it->first;
  
            ds.merge(set_u, set_v);
        }
    }
  
    return mst_wt;
}

void kodPrufer(int **stablo, int n) {
    int static stani = 0;
    int cvor[n] = {0};

    for(int i=0; i<n; i++) {
        for(int j=0; j<n; j++) {
            if(stablo[i][j])
                cvor[i]++;
        }
    }

    for(int i=0; i<n; i++) {
        if(cvor[i] >= 2) {
            break;
        }
    }

    for(int k=0; k<n; k++) {
        if(cvor[k] >= 2) {
            for(int i=0; i<n; i++) {
                if(cvor[i] == 1) {
                    for(int j=0; j<n; j++) {
                        if(stablo[i][j] == 1) {
                            cout << j+1;
                            stani++;
                            if(stani != (n-2)) {
                                cout << ", ";
                            }
                        }
                        stablo[i][j] = 0;
                        stablo[j][i] = 0;
                    }
                    break;
                }
            }
            break;
        }
    }

    for(int i=0; i<n; i++) {
        if(cvor[i] >= 2) {
            kodPrufer(stablo, n);
        }
    }
    return;
}
  
  
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

    // for(int i=0; i<n; i++) {
    //     for(int j=0; j<n; j++) {
    //         cout << matrica[i][j] << " ";
    //     }
    //    cout << endl;
    // }

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
  
        // cout << "Edges of MST are \n";
        int mst_wt = g.kruskalMST();

        //for(int z=0; z<n*n; z++) {
        //    cout << pomoc[z] << " ";
        //}
        //cout << endl;

        // cout << "Polje: ";
        // for(int i=0; i<n*n; i++) {
        //     cout << pomoc[i] << " ";
        // }
        // cout << endl;

    for(int i=0; i<n*n; i=i+2) {
        stablo[pomoc[i]][pomoc[i+1]] = 1;
        stablo[pomoc[i+1]][pomoc[i]] = 1;
        //cout << pomoc[i] << " " << pomoc[i+1] << endl;
    }
    stablo[0][0] = 0;

     cout << "Stablo:" << endl;
     for(int i=0; i<n; i++) {
         for(int j=0; j<n; j++) {
             cout << stablo[i][j] << " ";
         }
         cout << endl;
     }

    cout << "Pruferov kod minimalnog razapinjuceg stabla: (";
    kodPrufer(stablo, n);
    cout << ")";

    //cout << "\nWeight of MST is " << mst_wt;

    } else {
        cout << "Graf G nije povezan graf" << endl;
    }
  
    return 0;
}