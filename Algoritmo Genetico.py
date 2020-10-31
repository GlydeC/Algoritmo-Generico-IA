import sys
import re
import random
from collections import deque, defaultdict

# Puede jugar con el tamaño de la poblacion y numero de generaciones
# Tambien el codigo esta escrito para soportar diferentes problemas, ergo, puede cambiar el peso max, los valores del array de pesos y valores
# Puede agregar o substraer elementos del array de pesos y valores, aunque solo hay que tomar en cuenta que el tamaño de los dos arrays TIENE que ser igual
pesos = [ 42, 23, 21, 15, 7 ]
valor = [ 100, 60, 70, 15, 15 ]

# Considera que el tamaño de la poblacion es el doble, ya que se el tamaño se duplicara con la inversa de cada individuo que se genero.
# Si se generan individuos iguales con la inversa no se van a agregar a la generacion inicial por lo que pueden ser menos del doble.
poblacion_tamaño = 2
peso_max = 60
generaciones_max = 10

def randomizar_idividuo(p): 

    key1 = "" 

    for i in range(p): 
        temp = str(random.randint(0, 1)) 
        key1 += temp 
    return(key1) 

def dividir_individuo(individuo):
    return [char for char in individuo] 

def juntar_individuo(individuo):
    new = ""
    for x in individuo: 
        new += x    
    return new

def generarPoblacionInicial():
    poblacion = list()
    for i in range(poblacion_tamaño):
        poblacion.append(randomizar_idividuo(len(valor)))
    return poblacion

def generarInversos(poblacion):
    for x in range(len(poblacion)):
        individuo = dividir_individuo(poblacion[x])
        for y in range(len(dividir_individuo(individuo))):
            if individuo[y] == '1':
                individuo[y] = '0'
            else:
                individuo[y] = '1'
        poblacion[x] = juntar_individuo(individuo)
    
    return poblacion

def restriccion_peso(peso_individuo):
    if peso_individuo <= peso_max:
        return True
    return False

def encontrar_peso_valor(poblacion):
    peso_individuo = [0]*len(poblacion)*2
    valor_individuo = [0]*len(poblacion)*2
    peso_restriccion = [False]*len(poblacion)*2

    for x in range(len(poblacion)): 
        individuo = dividir_individuo(poblacion[x])
        for y in range(len(dividir_individuo(individuo))):
            if individuo[y] == '1':
                peso_individuo[x] += pesos[y]
                valor_individuo[x] += valor[y]
        if restriccion_peso(peso_individuo[x]):
                    peso_restriccion[x] = True

    
    return peso_individuo, valor_individuo, peso_restriccion           
                            
def checar_repetido_lista(lista, individuo):
    for i in range(len(lista)):
        if lista[i] == individuo:
            return True
    return False

def cruzar_individuos(i1, i2):
    individuo1 = dividir_individuo(i1)
    individuo2 = dividir_individuo(i2)
    individuo3 = [""]*len(individuo1)

    for x in range(len(individuo1)):
        if individuo1[x] == individuo2[x]:
            individuo3[x] = individuo1[x]
        elif random.randint(1,2) == 1:
            individuo3[x] = individuo1[x]
        else:
            individuo3[x] = individuo2[x]
    return juntar_individuo(individuo3)
            
def mutar_individuo(ind):
    individuo = dividir_individuo(ind)
    nuevo_individuo = [""]*len(individuo)

    for x in range(len(individuo)):
        # 15% de probabilidad de que mute un binario del individuo
        if random.randint(0,100) >= 85:
            if individuo[x] == '1':
                nuevo_individuo[x] = '0'
            else:
                nuevo_individuo[x] = '1'    
        else:
            nuevo_individuo[x] = individuo[x]

    return juntar_individuo(nuevo_individuo)   

def generar_hijos(generacion_anterior, generacion_anterior_valores):
    ganadores = list()
    # Seleccionar individuos para cruzar
    for x in range(len(generacion_anterior)):
        # Tomamos el individuo actual y lo comparamos con uno random de la lista
        y = random.randint(0, len(generacion_anterior_valores) -1)
        if generacion_anterior_valores[x] >= generacion_anterior_valores[y]:
            if not checar_repetido_lista(ganadores, generacion_anterior[x]):
                ganadores.append(generacion_anterior[x])
        else:
            if not checar_repetido_lista(ganadores, generacion_anterior[y]):
                ganadores.append(generacion_anterior[y])
    
    # Cruzar
    generacion_nueva = list()
    for x in range(len(ganadores)):
        # Cruzamos con dos ganadores al azar
        y = random.randint(0, len(ganadores) -1)
        z = random.randint(0, len(ganadores) -1)

        hijo1 = cruzar_individuos(ganadores[x], ganadores[y])
        hijo2 = cruzar_individuos(ganadores[x], ganadores[z])

        if not checar_repetido_lista(generacion_nueva, hijo1):
            generacion_nueva.append(hijo1)
        if not checar_repetido_lista(generacion_nueva, hijo2):
            generacion_nueva.append(hijo2)

    # Mutar
    for x in range(len(ganadores)):
        mutacion = mutar_individuo(ganadores[x])

        if not checar_repetido_lista(generacion_nueva, mutacion):
            generacion_nueva.append(mutacion)

    for i in range(len(generacion_nueva)):
        print(dividir_individuo(generacion_nueva[i]))

    return generacion_nueva

def encontrar_solucion(poblacion, poblacion_valores):
    individuo_maximo = 0
    valor_maximo = 0
    for x in range(len(poblacion)):
        if poblacion_valores[x] > valor_maximo:
            individuo_maximo = x
            valor_maximo = poblacion_valores[x]
    
    return poblacion[individuo_maximo], valor_maximo

def main():
    # Generar la poblacion inicial
    poblacion_inicial = generarPoblacionInicial()
    for x in range(len(poblacion_inicial)): 
        print (dividir_individuo(poblacion_inicial[x]))

    print("")

    temp = list(poblacion_inicial)

    poblacion_inicial_inversa = generarInversos(temp)

    for x in range(len(poblacion_inicial_inversa)): 
        print (dividir_individuo(poblacion_inicial_inversa[x]))

    print("")
    
    poblacion_inicial = poblacion_inicial + poblacion_inicial_inversa

    
    for x in range(len(poblacion_inicial)): 
        print (dividir_individuo(poblacion_inicial[x]))
    # Evaluar la poblacion inicial
    # Guarda una lista de los pesos, valores de cada individuo
    # Ademas guarda un booleano que indica si ese individuo cumple con la restriccion peso
    peso_individuo, valor_individuo, peso_restriccion = encontrar_peso_valor(poblacion_inicial)

    individuo_apto = list()
    individuo_apto_valor = list()

    for i in range(len(peso_individuo)):
        print("")
        print(f"El valor del individuo {i+1} es: {valor_individuo[i]} con un peso de: {peso_individuo[i]}")
        if peso_restriccion[i]:
            print("Cumple con la restriccion peso")
            if not checar_repetido_lista(individuo_apto, poblacion_inicial[i]):
                individuo_apto.append(poblacion_inicial[i])
                individuo_apto_valor.append(valor_individuo[i])
    
    print("INDIVIDUOS APTOS")
    for i in range(len(individuo_apto)):
        print(dividir_individuo(individuo_apto[i]))

    generacion_anterior = list(individuo_apto)
    generacion_anterior_valores = list(individuo_apto_valor)

    for gen in range(generaciones_max):
        print(f"Gen {gen+1}")
        peso_individuo.clear()
        valor_individuo.clear()
        peso_restriccion.clear()
        individuo_apto.clear()
        individuo_apto_valor.clear()
        # Cruzamos y mutamos para crear una nueva generacion
        generacion_nueva = generar_hijos(generacion_anterior, generacion_anterior_valores)
        # Evaluamos la nueva generacion
        peso_individuo, valor_individuo, peso_restriccion = encontrar_peso_valor(generacion_nueva)

        for i in range(len(generacion_nueva)):
            if peso_restriccion[i]:
                if not checar_repetido_lista(individuo_apto, generacion_nueva[i]):
                    individuo_apto.append(generacion_nueva[i])
                    individuo_apto_valor.append(valor_individuo[i])

        generacion_anterior = list(individuo_apto)
        generacion_anterior_valores = list(individuo_apto_valor)
        
    individuo_solucion, valor_solucion = encontrar_solucion(generacion_anterior, generacion_anterior_valores)

    print(f" La solucion al problema es: {individuo_solucion}")
    print(f" Con un valor de: {valor_solucion}")


main()