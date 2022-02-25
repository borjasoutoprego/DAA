# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 15:53:50 2021

@author: Carmen Lozano López, Borja Souto Prego, Nina López Laudenbach
"""
from numpy.random import seed
from numpy.random import randint
import numpy
import copy
import time
from time import time_ns
from prettytable import PrettyTable 
import math

def perfcounter_ns():
    '''Calcula el tiempo en nanosegundos'''
    return time.perf_counter() * (10**9)

def insertionSort(v):
    '''Ordena los elementos con el método de inserción'''
    a = v.copy()
    n = len(a)
    for i in range(1,n):
        x = a[i]
        j = i-1
        while j >= 0 and a[j] > x:
            a[j+1] = a[j]
            j = j-1
            a[j+1] = x
    return a
        
def bubbleSort(v):
    '''Ordena los elementos con el método de la burbuja'''
    a = v.copy()
    n = len(a)
    for i in range(1,n):
        for j in range(0,n-i):
            if a[j+1] < a[j]:
                a[j], a[j+1] = a[j+1], a[j]
    return a
                
def test(lista, funcion, nombre, lista_ordenada):  
    '''Valida una función de ordenación'''
    assert(funcion(lista)==lista_ordenada)
    print ("Input: {}".format(lista))
    print("Output", nombre, ": {}".format(funcion(lista)), "\n")

def tabla_resultados(elementos, umbral, k, algoritmo, orden, f_sub, f_ajustada,
                     f_sobre, cotas):
    '''Devuelve una tabla con los tiempos y sus correspondientes cotas'''
    #Crea la tabla
    tabla = PrettyTable()
    tabla.field_names = ['n', 't(n)', 't(n) /'+cotas[0], 't(n) /'+cotas[1] ,
                         't(n) /'+cotas[2]]
    #Define tipo de vector
    for n in elementos:
        if orden=="desordenado":
            array = randint(-n,n,n)
        elif orden=="ascendente":
            array = numpy.arange(-n/2,n/2)
        elif orden=="descendente":
            array = numpy.arange(n/2,-n/2,-1)
        else:
            raise ValueError
        #Cálculo tiempos
        t1 = perfcounter_ns()
        algoritmo(array)
        t2 = perfcounter_ns()
        tiempo = t2-t1
        if tiempo < umbral:
            t1 = perfcounter_ns()
            for c in range(k):
                algoritmo(array)
            t2 = perfcounter_ns()
            tiempo = (t2-t1) / k
            tiempo2 = str(tiempo)+"*" 
            tabla.add_row([n, tiempo2, tiempo/float(f_sub(n)), 
                           tiempo/float(f_ajustada(n)), tiempo/float(f_sobre(n))])
        else:
            tabla.add_row([n, tiempo, tiempo/float(f_sub(n)), 
                           tiempo/float(f_ajustada(n)), tiempo/float(f_sobre(n))])
    return tabla

if __name__ =="__main__":
    
    #Validación de las funciones
    tests = [ [-9,4,13,-1,-5], [6,-3,-15,5,4,5,2], [13,4], [9], 
             [7,6,6,5,4,3,2,1], [1,2,3,4,4,5,6,7], [-60,50,44,8,0,-3,-36]]
    for t in tests:
        test(t, bubbleSort, "bubble sort", sorted(t))
        test(t, insertionSort, "insertion sort", sorted(t))
    print("Comprobación aleatoria:")
    seed(1)
    sizes = [5,10,15]
    for size in sizes:
        #crea un array de tamaño size, con elementos aleatorios entre -10 y 10
        array = list(randint(-10,10,size))
        test(array, bubbleSort, "bubble sort", sorted(array))
        test(array, insertionSort, "insertion sort", sorted(array))
        
    #Cálculo de tiempos
    elementos = [100, 200, 400, 800, 1600, 3200, 6400] 
    u = 500000
    k = 1000
    #Vectores desordenados
    print("Desordenado bubblesort:")
    print(tabla_resultados(elementos, u, k, bubbleSort, "desordenado",
                            lambda x:x, lambda x:x**2, lambda x:math.log(x)*x**2,
                            ["n", "n**2", "log(n)*n**2"]))
    print("Desordenado insertionsort: ")
    print(tabla_resultados(elementos, u, k, insertionSort, "desordenado", 
                            lambda x:x, lambda x:x**2, lambda x:math.log(x)*x**2,
                            ["n", "n**2", "log(n)*n**2"]))
    #Vectores ascendentes
    print("Ascendente bubblesort: ")
    print(tabla_resultados(elementos, u, k, bubbleSort, "ascendente", 
                            lambda x:x, lambda x:x**2, lambda x:math.log(x)*x**2, 
                            ["n", "n**2", "log(n)*n**2"]))
    print("Ascendente insertionsort:")
    print(tabla_resultados(elementos, u, k, insertionSort, "ascendente", 
                            lambda x:math.log(x), lambda x:x, lambda x:x**1.5,
                            ["log(n)", "n", "n**1.5"]))
    #Vectores descendentes
    print("Descendente bubblesort: ")
    print(tabla_resultados(elementos, u, k, bubbleSort, "descendente",
                            lambda x:x, lambda x:x**2, lambda x:math.log(x)*x**2, 
                            ["n", "n**2", "log(n)*n**2"]))
    print("Descendente insertionsort:")
    print(tabla_resultados(elementos, u, k, insertionSort, "descendente", 
                            lambda x:x, lambda x:x**2, lambda x:math.log(x)*x**2,
                            ["n", "n**2", "log(n)*n**2"]))
