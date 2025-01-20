#include<iostream>
#include<iomanip>

using namespace std;

double rezFun(double a0, double a1, double l1, double l2, int n) {
    double rezultat;
    double b0 = a0;
    double b1 = a1;

    if(n == 0) return a0;
    if(n == 1) return a1;

    for(int i=2; i<=n; i++) {
        rezultat = l1 * b1 + l2 * b0;
        b0 = b1;
        b1 = rezultat;
    }

    return rezultat;
}

int main() {
    int n;

    do {
        cout << "Unesite nenegativan cijeli broj: ";
        cin >> n;
    } while(n < 0);

    double b0, b1, b2, c0, c1, c2;
    
    cout << "Unesite vrijednost broja b_0: ";
    cin >> b0;
    cout << "Unesite vrijednost broja b_1: ";
    cin >> b1;
    cout << "Unesite vrijednost broja b_2: ";
    cin >> b2;
    
    cout << "Unesite vrijednost broja c_0: ";
    cin >> c0;
    cout << "Unesite vrijednost broja c_1: ";
    cin >> c1;
    cout << "Unesite vrijednost broja c_2: ";
    cin >> c2;

    double l1, l2;

    l1 = (c0 * b2 - b0 * c2) / (b1 * c0 - b0 * c1);
    l2 = (b1 * c2 - c1 * b2) / (b1 * c0 - b0 * c1);

    double bn, bn0, bn1;

    bn = rezFun(b0, b1, l1, l2, n);

    cout << setprecision(20);
    cout << "Vrijednost broja b_n: " << bn << endl;

    return 0;
}