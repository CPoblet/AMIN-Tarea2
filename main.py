import math
import sys
import numpy as np
import pandas as pd

# py main.py berlin52.tsp.txt 0 10 100 0.1 2.5 0.9

def solucion_calcular_costo(n, s, c):
    aux = c[s[n-1]][s[0]]
    for i in range(n-1):
        aux += c[s[i]][s[i+1]]
    return aux

def main(argv):
    if (len(argv) == 8):
        archivo_entrada = argv[1]
        seed = int(argv[2])
        n = int(argv[3])
        iteraciones = int(argv[4])
        alpha = float(argv[5])
        beta = float(argv[6])
        q0 = float(argv[7])

        np.set_printoptions(threshold=sys.maxsize)
        np.set_printoptions(suppress=True)
        np.random.seed(seed=seed)
        matriz_coordenadas = pd.read_table(archivo_entrada, header=None, skiprows=6, skipfooter=1, delim_whitespace=True, engine='python').drop(0, axis=1).to_numpy(dtype=float)

        num_variables = matriz_coordenadas.shape[0]
        matriz_distancias = np.full((num_variables, num_variables), fill_value= -1, dtype=float)
        for i in range(num_variables-1):
            for j in range(i+1, num_variables):
                matriz_distancias[i][j] = np.sqrt(np.sum(np.square(matriz_coordenadas[i]-matriz_coordenadas[j])))
                matriz_distancias[j][i] = matriz_distancias[i][j]
        matriz_distancias = np.around(matriz_distancias, decimals=4)
        ##print(matriz_distancias)
        matriz_heuristica = 1/matriz_distancias
        matriz_heuristica[matriz_heuristica == -1] = 0
        ##print(matriz_heuristica)

        solucion_mejor = np.arange(0, num_variables)
        np.random.shuffle(solucion_mejor)

        solucion_mejor_costo = solucion_calcular_costo(num_variables, solucion_mejor, matriz_distancias)

        Tij0 = 1/(num_variables*solucion_mejor_costo)
        matriz_feronoma = np.full_like(matriz_distancias, fill_value=Tij0, dtype=float)
        ##print(matriz_feronoma)

        matriz_memoria = np.zeros((n, num_variables), dtype=int)

        matriz_colonia = np.zeros((n, num_variables), dtype=int)
        g = 1
        while g <= iteraciones:
            ##print(g)
            for i in range(len(matriz_colonia)):
                aux = np.random.randint(0, num_variables)
                matriz_colonia[i][0] = aux
                matriz_memoria[i][aux] = 1
            ##print(matriz_colonia)
            ##print(matriz_memoria)
            num_hormigas = matriz_colonia.shape[0]
            for i in range(1, num_variables):
                for j in range(num_hormigas):
                    q = np.random.rand()
                    TxN = transicion(matriz_colonia[j][i-1], matriz_feronoma, matriz_heuristica, matriz_memoria[j], beta)
                    if q <= q0:
                        j0 = np.random.choice(np.where(TxN == TxN.max())[0])
                    else:
                        j0 = ruleta(TxN)

                    Tij = (1-alpha)*matriz_feronoma[matriz_colonia[j][i]][j0] + alpha*Tij0
                    matriz_feronoma[matriz_colonia[j][i-1]][j0] = Tij
                    matriz_memoria[j][j0] = 1
                    matriz_colonia[j][i] = j0
            ##print(matriz_feronoma)
            ##print(solucion_mejor_costo)
            for i in matriz_colonia:
                costo = solucion_calcular_costo(num_variables, i, matriz_distancias)
                if costo <= solucion_mejor_costo:
                    solucion_mejor_costo = costo
                    solucion_mejor = i
            matriz_feronoma = matriz_feronoma*(1-alpha)
            deltaT = 1/(solucion_mejor_costo)
            for i in range(len(solucion_mejor)-1):
                matriz_feronoma[solucion_mejor[i]][solucion_mejor[i+1]] = (1-alpha)*matriz_feronoma[solucion_mejor[i]][solucion_mejor[i+1]] + alpha*deltaT
            g+=1
            matriz_memoria = np.full_like(matriz_memoria, fill_value=0, dtype=int)
            print(solucion_mejor_costo)

        print(solucion_mejor_costo)
        print(solucion_mejor)


    else:
        print('Error: Parámetros incorrectos')

def ruleta(TxN):
    p = np.full_like(TxN, 0, dtype=np.longdouble)
    TxN_sum = np.sum(TxN)
    for j in range(len(TxN)):
        p[j] = TxN[j]/TxN_sum
    index = np.where(np.random.uniform(min(p), max(p)) < p)[0]
    aux = 0
    for j in index:
        if p[j] > aux:
            j0 = j
            aux = p[j]
    return j0


def transicion(i, feronoma, heuristica, memoria, beta):
    N = np.full_like(memoria, 0, dtype=np.longdouble)
    for j in range(len(N)):
        if memoria[j] == 0:
            Tij = feronoma[i][j]
            Nij = heuristica[i][j]
            Nij_powB = math.pow(Nij, beta)
            TxN = Tij*Nij_powB
            N[j] = TxN
    return N

if __name__ == '__main__':
    print(sys.argv)
    main(sys.argv)