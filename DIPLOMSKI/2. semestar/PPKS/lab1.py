import numpy as np  # Učitaj biblioteku za numeričke operacije
import matplotlib.pyplot as plt  # Učitaj biblioteku za iscrtavanje

jmbag = "1191249229"

x0 = -5
xn = []
for digit in jmbag:
    xn.append(int(digit))
# xn = [1, 1, 9, 1, 2, 4, 9, 2, 2, 9]

# Grafički prikaz rezultata
plt.figure(figsize=(12, 8))

# Diskretni signal
signal = np.array(xn)  # [1 1 9 1 2 4 9 2 2 9]
n = np.arange(x0, len(xn) + x0)  # [-5 -4 -3 -2 -1 0 1 2 3 4]
plt.subplot(5, 2, 1)
plt.stem(n, signal)
plt.title("Originalni signal")
plt.xlabel("n")
plt.ylabel("x[n]")
plt.grid()
plt.xticks(np.arange(x0, len(n) + x0, 1))
plt.yticks(np.arange(0, 10, 2))
plt.xlim(x0 - 0.5, len(n) + x0 - 0.5)
plt.ylim(-1, 10)

# Zrcaljenje: x[-n]
zrcaljenje = signal[::-1]   # [9 2 2 9 4 2 1 9 1 1]
n_zrcaljenje = n[::-1] * (-1)   # [-4 -3 -2 -1 0 1 2 3 4 5]
plt.subplot(5, 2, 2)
plt.stem(n_zrcaljenje, zrcaljenje)
plt.title("Zrcaljeni signal x[-n]")
plt.xlabel("n")
plt.ylabel("x[n]")
plt.grid()
plt.xticks(np.arange(-4, 6, 1))
plt.yticks(np.arange(0, 10, 2))
plt.xlim(x0 + 0.5, len(n) + x0 + 0.5)
plt.ylim(-1, 10)

# Skaliranje: x[3n]
signal_scaled_3n = []
n_skal_3n = []
for vrijednost in n:
    if ((vrijednost * 3) >= x0) and ((vrijednost * 3) < len(xn) + x0):
        n_skal_3n.append(vrijednost)
        for i, element in enumerate(n):
            if element == (vrijednost*3):
                signal_scaled_3n.append(xn[i])
# signal_scaled_3n = [9, 4, 2]
# n_skal_3n = [-1, 0, 1]
plt.subplot(5, 2, 3)
plt.stem(n_skal_3n, signal_scaled_3n)
plt.title("Skalirani signal x[3n]")
plt.xlabel("n")
plt.ylabel("x[n]")
plt.grid()
plt.xticks(np.arange(x0 // 3 +0.5, len(xn) + x0 - 3, 0.5))
plt.yticks(np.arange(0, 10, 2))
plt.ylim(-1, 10)

# Skaliranje: x[n/2]
signal_scaled_n2_0 = np.array([signal[i // 2] if i % 2 == 0 else 0 for i in range(len(signal) * 2)])  # [1 0 1 0 9 0 1 0 2 0 4 0 9 0 2 0 2 0 9 0]
signal_scaled_n2 = signal_scaled_n2_0[:-1]  # [1 0 1 0 9 0 1 0 2 0 4 0 9 0 2 0 2 0 9]
n_skal = 2 * n   # [-10  -8  -6  -4  -2   0   2   4   6   8]
n_skal_n2 = np.arange(n_skal[0], n_skal[-1] + 1)    # [-10 -9 -8 -7 -6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6 7 8]
plt.subplot(5, 2, 4)
plt.stem(n_skal_n2, signal_scaled_n2)
plt.title("Skalirani signal x[n/2]")
plt.xlabel("n")
plt.ylabel("x[n]")
plt.grid()
plt.xticks(np.arange(x0 * 2, len(xn) - 1, 1))
plt.yticks(np.arange(0, 10, 2))
plt.ylim(-1, 10)

# Pomak: x[n+3] (ulijevo)
n_pomak_3 = n - 3   # [-8 -7 -6 -5 -4 -3 -2 -1 0 1]
plt.subplot(5, 2, 5)
plt.stem(n_pomak_3, signal)
plt.title("Pomaknuti signal x[n+3] (ulijevo)")
plt.xlabel("n")
plt.ylabel("x[n]")
plt.grid()
plt.xticks(np.arange(x0 - 3, len(xn) + x0 - 3, 1))
plt.yticks(np.arange(0, 10, 2))
plt.ylim(-1, 10)

plt.tight_layout()
plt.show()