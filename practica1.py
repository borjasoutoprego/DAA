"""

@author: Borja Souto Prego, Carmen Lozano López, Nina López Laudenbach
"""
# -*- coding: utf-8 -*-

#importamos librerías necesarias
import math
import time
from prettytable import PrettyTable 

def fib_recursive(n):
    '''Obtiene el valor n de la secuencia de Fibonacci de forma recursiva'''
    if n < 2:
        return n
    else:
        return fib_recursive(n-1) + fib_recursive(n-2)
  
    
def fib_iterative(n):
    '''Obtiene el valor n de la secuencia de Fibonacci de forma iterativa'''
    if n==0:
        return 0
    a=0
    b=1
    i=2
    while i<n:
        aux=a
        a=b
        b=b+aux
        i=i+1 
    return a+b


def fib_binet(n):
    '''Obtiene el valor n de la secuencia de Fibonacci con la fórmula de Binet'''
    Phi = (1 + math.sqrt(5))/2
    Tau = (1 - math.sqrt(5)/2)
    return round((math.pow(Phi, n) - math.pow(Tau, n)) / math.sqrt(5))


def timetime_ns():
    '''Conversión del tiempo a nanosegundos'''
    return time.time() * (10**9)


def make_table(lista, algoritmo, umbral, k, f_sub, f_ajustada, f_sobre):
    tabla = PrettyTable()
    for n in lista:
        t1 = timetime_ns()
        algoritmo(n)
        t2 = timetime_ns()
        tiempo = t2-t1
        if tiempo >= umbral:
            if f_sub is not None:
                tabla.add_row([n, tiempo, tiempo/float(f_sub(n)), tiempo/float(f_ajustada(n)), tiempo/float(f_sobre(n))])
            else:
                tabla.add_row([n, tiempo, '--', tiempo/float(f_ajustada(n)), tiempo/float(f_sobre(n))])
        
        elif tiempo < umbral: # 500000 nanosegundos = 500 microsegundos
            t1 = timetime_ns()
            for c in range(k):
                algoritmo(n)
            t2 = timetime_ns()
            tiempo = (t2-t1) / k
            if f_sub is not None:
                tabla.add_row([n, tiempo, tiempo/float(f_sub(n)), tiempo/float(f_ajustada(n)), tiempo/float(f_sobre(n))])
            else:
                tabla.add_row([n, tiempo, '--', tiempo/float(f_ajustada(n)), tiempo/float(f_sobre(n))])
    return tabla


if __name__=="__main__":

#apartado 2: Validación de las funciones
    print("Validación de que los algoritmos funcionan correctamente:")
    for n in range(10):
        print("Fibonacci_recursive({}) = {} ".format(n,fib_recursive(n)))
    print('')
    for n in range(10):
        print("Fibonacci_iterative({}) = {} ".format(n,fib_iterative(n)))
    print('')
    for n in range(10):
        print("Fibonacci_binet({}) = {} ".format(n,fib_binet(n)))
    print('')

#apartado 3
    #tiempos y tabla para la forma recursiva
    sucesiones_r = [2,4,8,16,32]   
    tabla = make_table(sucesiones_r, fib_recursive, 500000, 10000, lambda x: math.pow(x,2), lambda x: math.pow(1.6180, x), lambda x: math.pow(2, x))
    tabla.field_names = ['n', 't(n)', 't(n) / math.pow(n,2)', 't(n) / math.pow(1.6180, n)' , 't(n) / math.pow(2,n)']
    print('Tabla de la función recursiva: \n', tabla, '\n', '*'*50)

    #tiempos y tabla para la fórmula de Binet
    sucesiones_b = [2,4,8,16,32,64,128]        
    tabla1 = (make_table(sucesiones_b, fib_binet, 500000, 10000, None, lambda x: 1, lambda x: math.log(x)))
    tabla1.field_names = ['n', 't(n)', '--', 't(n) / 1' , 't(n) / math.log(n)']
    print('Tabla de la función de binet: \n', tabla1, '\n', '*'*50)
    
    # tiempos y tabla para la forma iterativa   
    tabla2 = (make_table(sucesiones_b, fib_iterative, 500000, 10000, lambda x: math.log(x), lambda x: x, lambda x: math.pow(x,2)))
    tabla2.field_names = ['n', 't(n)', 't(n) / math.log(n)', 't(n) / n' , 't(n) / math.pow(n, 2)']
    print('Tabla de la función iterativa: \n', tabla2)



    
