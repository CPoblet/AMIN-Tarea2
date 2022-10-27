import sys
from textwrap import fill
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
        i = int(argv[4])
        alpha = float(argv[5])
        beta = float(argv[6])
        q0 = float(argv[7])

        ##np.set_printoptions(threshold=sys.maxsize)
        np.random.seed(seed=seed)
        matriz_coordenadas = pd.read_table(archivo_entrada, header=None, skiprows=6, skipfooter=1, delim_whitespace=True, engine='python').drop(0, axis=1).to_numpy(dtype=float)
        print(matriz_coordenadas)

        num_variables = matriz_coordenadas.shape[0]
        matriz_distancias = np.full((num_variables, num_variables), fill_value= 0, dtype=float)
        for i in range(num_variables-1):
            for j in range(i+1, num_variables):
                matriz_distancias[i][j] = 1/np.sqrt(np.sum(np.square(matriz_coordenadas[i]-matriz_coordenadas[j])))
                matriz_distancias[j][i] = matriz_distancias[i][j]
        print(matriz_distancias)

        solucion_mejor = np.arange(0, num_variables)
        np.random.shuffle(solucion_mejor)

        solucion_mejor_costo = solucion_calcular_costo(num_variables, solucion_mejor, matriz_distancias)
        solucion_mejor_iteracion = 0

        Tij0 = 1/(num_variables*solucion_mejor_costo)
        matriz_feronoma = np.full_like(matriz_distancias, fill_value=Tij0, dtype=float)
        print(matriz_feronoma)
        

    else:
        print('Error: Parámetros incorrectos')


if __name__ == '__main__':
    print(sys.argv)
    main(sys.argv)
