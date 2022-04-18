# -*- coding: utf-8 -*-
"""

@author: Borja Souto Prego, Carmen Lozano López, Nina López Laudenbach
"""
import numpy as np
from prettytable import PrettyTable 
import time
import math

def isMixtureDP(A, B, C):
    '''Valida que dos palabras se hayan mezclado correctamente '''
    n, m, s = len(A), len(B), len(C)
    if n + m != s:
        return False
    t = []    
    for f in range(n+1):
        t.append([])
        for c in range(m+1):
            t[f].append(False)
    t[0][0] = True
    for i in range(n+1):
        for j in range(m+1):
            t[i][j] = t[max(0, i-1)][j] or t[i][max(0, j-1)] 
            if t[i][j] and (i < n or j < m):
                k = i+j
                t[i][j] = False
                if i < n:
                    t[i][j] = (t[i][j] or (A[i] == C[k])) 
                if j < m:
                    t[i][j] = (t[i][j] or (B[j] == C[k]))
    return t[n][m]


def isMixtureCX(A, B, C):
    '''Valida que dos palabras se hayan mezclado correctamente '''
    n, m, s = len(A), len(B), len(C)
    if n+m != s:
        return False
    Known = {(0,0)} 
    Trial = [(0,0)] 
    while len(Trial) > 0:
        (i, j) = Trial.pop() 
        k = i+j
        if k >= s:
            return True
        if (i < n) and (A[i] == C[k]) and ((i+1, j) not in Known):
            Trial.append((i+1, j))
            Known.add((i+1, j))
        if (j < m) and (B[j] == C[k]) and ((i, j+1) not in Known):
            Trial.append((i, j+1))
            Known.add((i, j+1))
    
    return False

def create_word(n, alphabet=(0, 1)):
    '''Crea palabras de longitud n con el alfabeto indicado '''
    a = np.random.randint(low=0, high=len(alphabet), size=(n,))
    word = np.array(alphabet)[a].tolist()
    return word

def mix_words(a, b, valid=True):
    '''Mezcla dos strings o listas de enteros, de forma correcta o incorrecta según lo indicado'''
    new_word = []
    a_array = np.array(a)
    b_array = np.array(b)
    if not valid:
        np.random.shuffle(a_array)
        np.random.shuffle(b_array)
    a_index = 0
    b_index = 0
    while len(new_word) < len(a) + len(b):
        p = np.random.randint(2)
        if (p and a_index < len(a_array)) or b_index >= len(b_array):
            new_word.append(a_array[a_index])
            a_index += 1
        else:
            new_word.append(b_array[b_index])
            b_index += 1
    return new_word

def perfcounter_ns():
    '''Calcula el tiempo en nanosegundos'''
    return time.perf_counter() * (10**9)

def tabla_resultados(elementos, umbral, k, algoritmo, escenario, f_sub,f_ajustada, 
                     f_sobre, cotas):
    '''Devuelve una tabla con los tiempos y sus correspondientes cotas'''
    #Crea la tabla
    tabla = PrettyTable()
    tabla.field_names = ['n', 't(n)', 't(n) /'+cotas[0], 't(n) /'+cotas[1] ,
                         't(n) /'+cotas[2]]
    
    for n in elementos:
        if escenario == 1: 
            a=create_word(n)
            b=create_word(n) 
        elif escenario==2:
            a=create_word(n, range(256))
            b=create_word(n, range(256))
        elif escenario==3:
            a=create_word(n, range(n))
            b=create_word(n, range(n))
        else: print("Este escenario no existe")
        f =mix_words(a,b)
        #Cálculo tiempos 
        t1 = perfcounter_ns() 
        assert(algoritmo(a, b, f)==True) 
        t2 = perfcounter_ns() 
        tiempo = t2-t1  
        if tiempo < umbral: 
            t1 = perfcounter_ns() 
            for c in range(k): 
                assert(algoritmo(a, b, f)==True) 
            t2 = perfcounter_ns()
            tiempo = (t2-t1) / k
            tiempo2 = str(tiempo)+"*" 
            tabla.add_row([n, tiempo2, tiempo/float(f_sub(n)), 
                           tiempo/float(f_ajustada(n)), tiempo/float(f_sobre(n))])
        else:
            tabla.add_row([n, tiempo, tiempo/float(f_sub(n)), 
                           tiempo/float(f_ajustada(n)),tiempo/float(f_sobre(n))])
    return tabla

def test(funcion, A, B, C, name):
    '''Valida el funcionamiento de los algoritmos'''
    try:
        assert(funcion(A, B, C)==True)
        print(funcion(A, B, C), ": El resultado con ", C, " usando isMixture",
              name," es válido", sep="")
    except AssertionError:
        print("False: El resultado con ", C, " usando isMixture",name, 
              " es no válido", sep="")

if __name__ == "__main__":
    
    # Validación
    lista = ["HelloWorld", "WorldHello", "HWorellldo", "WorHellold", "HWeolrllod",
              "dlroWolleH", "oHelloWrld", "HelloWorlds", "HeloWorld", "HelloWooorld",
              "helloworld", "HELLOWORLD"]
    
    print("Validación del algoritmo:")
    for w in lista:
        test(isMixtureDP, "Hello", "World", w, "DP")
        test(isMixtureCX, "Hello", "World", w, "CX")
        print("\n")
    print("-"*70)
    
    # Cálculo de tiempos
    rep =[20, 40, 80, 160, 320, 640, 1280, 2560]
    
    print("Escenario 1: isMixtureCX")    
    print(tabla_resultados(rep, 500000, 1000, isMixtureCX, 1, lambda x:math.log(x), 
                            lambda x:x*1.2, lambda x:x**1.5,  
                            ["log(n)", "1.2*n", "n**1.5"]))
    
    print("Escenario 1: isMixtureDP")
    print(tabla_resultados(rep, 500000, 1000, isMixtureDP, 1, lambda x:x*math.log(x), 
                            lambda x: x**2, lambda x:(x**2)*math.log(x), 
                            ["n*log(n)", "n**2", "(n**2)*log(n)"])) 
    
    print("Escenario 2: isMixtureCX")
    print(tabla_resultados(rep, 500000, 1000, isMixtureCX, 2, lambda x:math.log(x), 
                            lambda x: 1.2*x, lambda x:x**1.5, ["log(n)", "1.2*n", "n**1.5"])) 
    
    print("Escenario 2: isMixtureDP")
    print(tabla_resultados(rep, 500000, 1000, isMixtureDP, 2, lambda x:x*math.log(x), 
                            lambda x: x**2, lambda x:(x**2)*math.log(x), 
                            ["n*log(n)", "n**2", "(n**2)*log(n)"])) 
    
    print("Escenario 3: isMixtureCX")
    print(tabla_resultados(rep, 500000, 1000, isMixtureCX, 3, lambda x:math.log(x), 
                            lambda x: 1.2*x, lambda x:x**1.5,
                            ["log(n)", "1.2*n", "n**1.5"])) 
    
    print("Escenario 3: isMixtureDP")
    print(tabla_resultados(rep, 500000, 1000, isMixtureDP, 3, lambda x: x*math.log(x), 
                            lambda x: x**2, lambda x:(x**2)*math.log(x), 
                            ["n*log(n)", "n**2", "(n**2)*log(n)"])) 
    
