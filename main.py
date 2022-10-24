import numpy as np
import pandas as pd
import sys

# py main.py berlin52.tsp.txt 0 10 100 0.1 2.5 0.9

def solucion_calcular_costo(n, s, c):
    aux = c[s[n-1]s[0]]
    for i in range(c-1):
        aux += c[s[i]s[i+1]]
    return aux

def main(argv):
    if (len(argv) == 8):
        archivo_entrada = argv[1]
        seed = argv[2]
        n = argv[3]
        i = argv[4]
        alpha = argv[5]
        beta = argv[6]
        q0 = argv[7]
        np.set_printoptions(threshold=sys.maxsize)
        matriz_coordenadas = pd.read_table(archivo_entrada, header=None, skiprows=6, skipfooter=1, delim_whitespace=True, engine='python').drop(0, axis=1).to_numpy(dtype=float)
        print(matriz_coordenadas)

        num_variables = matriz_coordenadas.shape[0]
        matriz_distancias = np.full((num_variables, num_variables), fill_value= 0, dtype=float)
        for i in range(num_variables-1):
            for j in range(i+1, num_variables):
                matriz_distancias[i][j] = 1/np.sqrt(np.sum(np.square(matriz_coordenadas[i]-matriz_coordenadas[j])))
                matriz_distancias[j][i] = matriz_distancias[i][j]
        print(matriz_distancias)


    else:
        print('Error: Parámetros incorrectos')


if __name__ == '__main__':
    print(sys.argv)
    main(sys.argv)
