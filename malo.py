import sys
import numpy as np
import pandas as pd

# py main.py berlin52.tsp.txt 0 10 100 0.1 2.5 0.9

def solucion_calcular_costo(n, s, c):
    aux = c[s[n-1]][s[0]]
    for i in range(n-1):
        aux += c[s[i]][s[i+1]]
        print(f'{i} : {aux}')
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

        solucion_optima = np.array([1,49,32,45,19,41,8,9,10,43,33,51,11,52,14,13,47,26,27,28,12,25,4,6,15,5,24,48,38,37,40,39,36,35,34,44,46,16,29,50,20,23,30,2,7,42,21,17,3,18,31,22])

        num_variables = matriz_coordenadas.shape[0]

        matriz_distancias = np.full((num_variables, num_variables), fill_value= 0, dtype=float)
        for i in range(num_variables-1):
            for j in range(i+1, num_variables):
                matriz_distancias[i][j] = np.sqrt(np.sum(np.square(matriz_coordenadas[i]-matriz_coordenadas[j])))
                matriz_distancias[j][i] = matriz_distancias[i][j]
        print(matriz_distancias)

        solucion_mejor = np.arange(0, num_variables)
        np.random.shuffle(solucion_mejor)

        """
        solucion_mejor_costo = solucion_calcular_costo(num_variables, solucion_mejor, matriz_distancias)
        solucion_mejor_iteracion = 0

        Tij0 = 1/(num_variables*solucion_mejor_costo)
        matriz_feronoma = np.full_like(matriz_distancias, fill_value=Tij0, dtype=float)
        print(matriz_feronoma) """
        
        print(matriz_distancias.shape)
        print(solucion_mejor)
        print(solucion_mejor.shape)
        print(solucion_optima-1)
        print(solucion_optima.shape)
        print(np.round(solucion_calcular_costo(num_variables, solucion_optima-1, matriz_distancias), decimals=4))


    else:
        print('Error: Parámetros incorrectos')


if __name__ == '__main__':
    print(sys.argv)
    main(sys.argv)
