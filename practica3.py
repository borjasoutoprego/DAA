# -*- coding: utf-8 -*-

import numpy as np
from prettytable import PrettyTable 
import time
import math

def find(lista_sets, u):
    '''Devuelve el set en el que está el elemento u'''
    for e in lista_sets:
        if u in e:
            return e

def merge(lista, A, B):
    '''Función merge que une dos conjuntos'''
    C = A|B
    lista.remove(A)
    lista.remove(B)
    lista.append(C)

def create_graph(n, max_distance=50):
    '''Funcion que crea grafos aleatorios'''
    a = np.random.randint(low=1, high=max_distance, size=(n,n))
    m = np.tril(a,-1) + np.tril(a, -1).T
    rows, cols = m.shape
    E = set([])
    V = set([])
    for i in range(rows): 
        V.add(i)
        for j in range(i+1, cols): 
            E.add((i,j,m[i][j]))
    return (V,E)

def perfcounter_ns():
    '''Calcula el tiempo en nanosegundos'''
    return time.perf_counter() * (10**9)

def kruskal(V, E):
    '''Función kruskal'''
    E = list(E)  
    E.sort(key=lambda x:x[2]) 
    T = set()      
    lista_sets =[] 
    for i in V: 
        S = {i} 
        lista_sets.append(S)
        
    for a in E:        
        if len(T) == len(V)-1: break
        #a = (E[0]) 
        Uset = find(lista_sets, a[0]) 
        Vset = find(lista_sets, a[1]) 
        if Uset != Vset: 
            merge(lista_sets, Uset, Vset)
            T.add(a)
        
    return T

def tabla_resultados(elementos, umbral, k, algoritmo, f_sub,f_ajustada, f_sobre,
                     cotas, crear_g, distancia):
    '''Devuelve una tabla con los tiempos y sus correspondientes cotas'''
    #Crea la tabla
    tabla = PrettyTable()
    tabla.field_names = ['n', 't(n)', 't(n) /'+cotas[0], 't(n) /'+cotas[1] ,
                         't(n) /'+cotas[2]]
    
    for n in elementos:
        grafo = crear_g(n,distancia)
        
        #Cálculo tiempos 
        t1 = perfcounter_ns() 
        algoritmo(grafo[0], grafo[1]) 
        t2 = perfcounter_ns() 
        tiempo = t2-t1  
        if tiempo < umbral: 
            t1 = perfcounter_ns() 
            for c in range(k): 
                algoritmo(grafo[0], grafo[1]) 
            t2 = perfcounter_ns()
            tiempo = (t2-t1) / k
            tiempo2 = str(tiempo)+"*" 
            tabla.add_row([n, tiempo2, tiempo/float(f_sub(n)), 
                           tiempo/float(f_ajustada(n)), tiempo/float(f_sobre(n))])
        else:
            tabla.add_row([n, tiempo, tiempo/float(f_sub(n)), 
                           tiempo/float(f_ajustada(n)),tiempo/float(f_sobre(n))])
    return tabla
    
def test(V, E, funcion, set_ordenado):  
    '''Valida la función de Kruskal'''
    assert(funcion(V,E)==set_ordenado)
    print("Input: Vértices:", V, "\nAristas:", E)
    print("Output" ": {}".format(funcion(V,E)),"\n")

if __name__=="__main__":
    
    V1 = {0,1,2,3}
    E1 = {(0, 2, 9), (2, 3, 2), (0, 3, 6), (1, 2, 4), (0, 1, 5), (1, 3, 3)}
    MST1_gold = {(2, 3, 2), (0, 1, 5), (1, 3, 3)}
    test(V1, E1, kruskal, MST1_gold)

    
    V2 = {0,1,2,3,4}
    E2 = {(3, 4, 6), (1, 2, 1), (0, 2, 9), (1, 4, 7), (0, 3, 4), (1, 3, 2), (2, 3, 3), (2, 4, 9), (0, 4, 8), (0, 1, 5)}
    MST2_gold = {(3, 4, 6), (1, 2, 1), (0, 3, 4), (1, 3, 2)}
    test(V2, E2, kruskal, MST2_gold)
    
    n=[20,40,80,160,320,640,1280,2560]

    print(tabla_resultados(n, 500000, 1000, kruskal, lambda x:x**2, lambda x: (x**2)*math.log(x), lambda x:x**3,
                            ["n**2", "(n**2)log(n)", "n**3"], create_graph, 50))



