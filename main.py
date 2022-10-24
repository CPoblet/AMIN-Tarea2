import numpy as np
import pandas as pd
import sys

# py main.py berlin52.tsp.txt 0 10 100 2.5 0.1 0.9

def main(argv):
    if (len(argv) == 8):
        archivo_entrada = argv[1]
        seed = argv[2]
        n = argv[3]
        i = argv[4]
        alpha = argv[5]
        beta = argv[6]
        q0 = argv[7]

        matriz_coordenadas = pd.read_table(archivo_entrada, header=None, skiprows=6, skipfooter=1, delim_whitespace=True, engine='python').drop(0, axis=1).to_numpy(dtype=float)
        print(matriz_coordenadas)

        num_variables = matriz_coordenadas.shape[0]
        matriz_distancias = np.full((num_variables, num_variables), fill_value= -1.0, dtype=float)
        for i in range(num_variables-1):
            for j in range(i+1, num_variables):
                print(matriz_coordenadas[i])
                print(matriz_coordenadas[j])
                print(np.sqrt(np.sum(np.square(matriz_coordenadas[i]-matriz_coordenadas[j]))))
                print('-----------------------')
                matriz_distancias[i][j] = np.sqrt(np.sum(np.square(matriz_coordenadas[i]-matriz_coordenadas[j])))
                matriz_distancias[j][i] = matriz_distancias[i][j]

        print(matriz_distancias)


    else:
        print('Error: Parámetros incorrectos')


if __name__ == '__main__':
    print(sys.argv)
    main(sys.argv)
