import numpy as np
import random as rd
import matplotlib.pyplot as plt

rd.seed(2025)

# Generar matriz de distancias simétrica
def matriz_distancias(n):
    dist = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i > j:
                a = rd.randint(100, 500)
                dist[i, j] = a
                dist[j, i] = a
            else:
                dist[i, j] = 0
    return dist


def f_individuo(n):
    ciudades = list(range(1, n))   
    rd.shuffle(ciudades)
    ciudades.insert(0, 0)          
    ciudades.append(0)             
    return ciudades


def f_evaluacion_individuo(camino, distancias):
    distancia_total = 0
    for i in range(len(camino) - 1):
        ciudad_actual = int(camino[i])
        ciudad_siguiente = int(camino[i + 1])
        distancia_total += distancias[ciudad_actual, ciudad_siguiente]
    return distancia_total


def f_evaluacion_poblacion(poblacion, distancias):
    t_poblacion = len(poblacion)
    dist_total_poblacion = np.zeros(t_poblacion)
    for i in range(t_poblacion):
        distancia_individuo = f_evaluacion_individuo(poblacion[i, :], distancias)
        dist_total_poblacion[i] = distancia_individuo
    return dist_total_poblacion


def f_ordena_poblacion(poblacion, distancias):
    dist_total_poblacion = f_evaluacion_poblacion(poblacion, distancias)
    poblacion = poblacion[np.argsort(dist_total_poblacion)]  
    return poblacion


def f_poblacion_inicial(n, t_poblacion, distancias):
    poblacion = np.zeros((t_poblacion, n + 1))
    for i in range(t_poblacion):
        poblacion[i, :] = f_individuo(n)
    poblacion = f_ordena_poblacion(poblacion, distancias)
    return poblacion

# Selección por torneo
def f_seleccion_torneo(poblacion, distancias, tamano_torneo=2):
    
    indices_torneo = rd.sample(range(len(poblacion)), tamano_torneo)
    
    # Evaluar los individuos del torneo
    evaluaciones = np.zeros(tamano_torneo)
    for i, indice in enumerate(indices_torneo):
        evaluaciones[i] = f_evaluacion_individuo(poblacion[indice], distancias)
    
    ganador = indices_torneo[np.argmin(evaluaciones)]
    return poblacion[ganador]

# Crossover para rutas
def f_crossover(padre, madre):
    n = len(padre) - 1
    corte = rd.randint(1, n - 2)

    padre = list(padre)
    madre = list(madre)

    hijo = padre[1:corte+1]

    for ciudad in madre:
        if ciudad not in hijo and ciudad != 0:
            hijo.append(ciudad)

    hijo = [0] + hijo + [0]
    return hijo

# Mutación por intercambio de ciudades
def f_mutacion(camino, prob_mutacion):
    nuevo_camino = camino.copy()
    if np.random.random() < prob_mutacion:
        i, j = rd.sample(range(1, len(nuevo_camino) - 1), 2)
        nuevo_camino[i], nuevo_camino[j] = nuevo_camino[j], nuevo_camino[i]
    return nuevo_camino

# Algoritmo genético completo con selección por torneo
def algoritmo_genetico(n, t_poblacion, generaciones, prob_mutacion, tamano_torneo=2):

    distancias = matriz_distancias(n)    
    poblacion = f_poblacion_inicial(n, t_poblacion, distancias)
    
    # Inicializar mejor solución global
    mejor_camino_global = np.copy(poblacion[0])
    mejor_distancia_global = f_evaluacion_individuo(mejor_camino_global, distancias)

    # Lista para almacenar las mejores distancias de cada generación
    mejores_distancias = []
     
    for gen in range(generaciones):
        distancias_poblacion = f_evaluacion_poblacion(poblacion, distancias)
        # Crear nueva población
        nueva_poblacion = np.zeros_like(poblacion)
        # conservar el mejor individuo
        nueva_poblacion[0] = poblacion[np.argmin(distancias_poblacion)]
        
       
        for i in range(1, t_poblacion):
            padre = f_seleccion_torneo(poblacion, distancias, tamano_torneo)
            madre = f_seleccion_torneo(poblacion, distancias, tamano_torneo)
            hijo = f_crossover(padre, madre)
            hijo = f_mutacion(hijo, prob_mutacion)            
            # Agregar a la nueva población
            nueva_poblacion[i] = hijo
        poblacion = f_ordena_poblacion(nueva_poblacion, distancias)        
        # Verificar si hemos encontrado una mejor solución
        mejor_actual = poblacion[0]
        mejor_distancia_actual = f_evaluacion_individuo(mejor_actual, distancias)
        if mejor_distancia_actual < mejor_distancia_global:
            mejor_camino_global = np.copy(mejor_actual)
            mejor_distancia_global = mejor_distancia_actual
            print(f"Generacion {gen+1}: Nueva solucion encontrada: {mejor_distancia_global}")
        
        # Guardar la mejor distancia de la generación actual
        mejores_distancias.append(mejor_distancia_global)
    
    # Graficar la convergencia
    plt.plot(mejores_distancias)
    plt.title("Convergencia del Algoritmo Genético")
    plt.xlabel("Generación")
    plt.ylabel("Mejor distancia")
    plt.show()
    
    return mejor_camino_global, mejor_distancia_global


n = 250  # número de ciudades
t_poblacion = 300
generaciones = 1000
prob_mutacion = 0.2
mejor_camino, mejor_distancia = algoritmo_genetico(n, t_poblacion, generaciones, prob_mutacion, tamano_torneo=2)


print("Mejor camino encontrado:", mejor_camino)
print("Distancia total del mejor camino:", mejor_distancia)





