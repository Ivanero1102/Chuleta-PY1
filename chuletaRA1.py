# ==============================================================================
#  CHULETA DEFINITIVA DE PYTHON (BASADA 100% EN TUS 3 ARCHIVOS DE CLASE)
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. IMPORTACIONES QUE USAS EN TODOS TUS CÓDIGOS
# ------------------------------------------------------------------------------
import threading              # Para crear hilos y Locks
from queue import Queue       # Para crear colas seguras entre hilos
import random                 # Para generar números aleatorios


# ------------------------------------------------------------------------------
# 2. VARIABLES GLOBALES Y PALABRA CLAVE 'global'
# ------------------------------------------------------------------------------
# Las variables declaradas fuera de las funciones son accesibles para leerlas,
# pero si quieres MODIFICAR su valor dentro de una función, debes poner 'global'.

texto = ""
textoCompleto = ""
terminamos = False
procesos = 0

def modificar_global():
    global procesos           # Obligatorio antes de cambiar su valor
    procesos = procesos - 1


# ------------------------------------------------------------------------------
# 3. HILOS (threading.Thread) - CREACIÓN Y ARRANQUE
# ------------------------------------------------------------------------------
def funcion_sin_datos():
    print("Ejecutando hilo sin argumentos")

def funcion_con_datos(dato1, dato2):
    print(f"Ejecutando hilo con {dato1} y {dato2}")

# A) Crear y arrancar un hilo SIN argumentos:
#    Fíjate en la coma vacía tras el nombre de la función
hilo1 = threading.Thread(target=funcion_sin_datos,)
hilo1.start()

# B) Crear y arrancar un hilo CON 1 argumento:
#    ¡MUY IMPORTANTE! Si pasas 1 solo argumento en args, pon una coma al final: (texto,)
hilo2 = threading.Thread(target=funcion_con_datos, args=(texto,))
hilo2.start()

# C) Crear y arrancar un hilo CON VARIOS argumentos:
hilo3 = threading.Thread(target=funcion_con_datos, args=("hola", "mundo"))
hilo3.start()

# D) Lanzar varios hilos iguales usando un bucle 'for'
cantidad = 3
for i in range(cantidad):
    hilo_bucle = threading.Thread(target=funcion_sin_datos,)
    hilo_bucle.start()


# ------------------------------------------------------------------------------
# 4. BLOQUEOS / LOCKS (threading.Lock) - EXCLUSIÓN MUTUA
# ------------------------------------------------------------------------------
# Sirve para que DOS HILOS NO MODIFIQUEN A LA VEZ una misma variable global.
# Si no pones Lock al sumar/restar variables globales, los datos se pueden pisar.

lock = threading.Lock()       # Se crea una vez fuera de las funciones

def agregar_texto_seguro(parte):
    lock.acquire()            # 1. Cierra el candado (ningún otro hilo entra aquí)
    global textoCompleto
    textoCompleto = textoCompleto + parte
    lock.release()            # 2. Abre el candado (ya puede pasar el siguiente hilo)


# ------------------------------------------------------------------------------
# 5. COLAS (Queue) - PASAR DATOS ENTRE HILOS DE FORMA SEGURA
# ------------------------------------------------------------------------------
# Las colas permiten que unos hilos metan datos (productores) y otros los saquen
# (consumidores) sin necesidad de usar Lock para la cola.

lista = Queue()               # Crea la cola vacía

# Meter un elemento al final de la cola (puede ser texto, una lista, etc.):
lista.put("dato")             # Metes strings
lista.put(["Golf", "19000"])  # Metes listas de 2 elementos

# Comprobar si la cola tiene elementos antes de sacar nada:
if not lista.empty():         # Devuelve True si está vacía; 'not lista.empty()' = hay datos
    elemento = lista.get()    # Saca y devuelve el primer elemento de la cola


# ------------------------------------------------------------------------------
# 6. PATRÓN 1: BUCLE DE ESCRITURA EN TIEMPO REAL
# ------------------------------------------------------------------------------
# Un hilo se queda vigilando en segundo plano hasta que 'terminamos' pasa a True.

# Variante A: Vigilando una Queue
def escritura_con_cola():
    textoReserva = ""
    while terminamos == False:
        if not lista.empty():
            textoReserva = textoReserva + lista.get()
            print("Texto agregado: " + textoReserva)

# Variante B: Vigilando cambios en una variable global con Lock
def escritura_con_lock():
    textoReserva = ""
    while terminamos == False:
        global textoCompleto
        if textoReserva != textoCompleto:
            lock.acquire()
            textoReserva = textoCompleto
            print("Texto agregado: " + textoCompleto)
            lock.release()


# ------------------------------------------------------------------------------
# 7. PATRÓN 2: PRODUCTOR - CONSUMIDOR CON CONTADOR DE HILOS ACTIVOS
# ------------------------------------------------------------------------------
# Clave de este patrón:
# - Los productores suman/meten cosas en la Queue y al acabar restan 1 a 'procesos'.
# - Los consumidores siguen vivos MIENTRAS queden cosas en la cola O queden
#   productores trabajando (procesos != 0).

def productor():
    for i in range(50):
        lista.put("item")
    
    # Al terminar su bucle, avisa de que hay un productor menos
    lock.acquire()
    global procesos
    procesos = procesos - 1
    lock.release()
    print("Cerrando linea de produccion")

def consumidor():
    global procesos
    while not lista.empty() or procesos != 0:   # Condición clave de parada
        if not lista.empty():
            item = lista.get()
            print("Consumido: " + str(item))
        else:
            print("No hay elementos")
    print("Cerrando consumidor")


# ------------------------------------------------------------------------------
# 8. TRUCOS Y OPERACIONES DE PYTHON QUE APARECEN EN TUS CÓDIGOS
# ------------------------------------------------------------------------------

# A) Partir un texto (String) exactamente por la mitad (Slicing):
palabra = "ExamenPython"
mitad = len(palabra) // 2     # '//' hace división entera (sin decimales)
parte1 = palabra[:mitad]      # Desde el principio hasta la mitad -> "Examen"
parte2 = palabra[mitad:]      # Desde la mitad hasta el final   -> "Python"

# B) Pedir datos por teclado (texto y números):
entrada_texto = input()                 # Siempre devuelve un String (texto)
entrada_numero = int(input())           # int() convierte el texto a número entero

# C) Bucle infinito hasta que el usuario escriba "-1" (Centinela):
while terminamos == False:
    print("Introduce un texto, -1 corta la ejecucion")
    texto = input()
    if texto != "-1":
        # Aquí lanzas los hilos para procesar 'texto'
        pass
    else:
        terminamos = True               # Cambia la bandera y detiene todos los while

# D) Listas paralelas y números aleatorios:
modelos = ["Golf", "Passat", "Polo", "Tiguan"]
precios = ["19000", "32000", "23000", "28000"]

aleatorio = random.randint(0, 3)        # Número entero aleatorio entre 0 y 3 (ambos incluidos)
coche = [modelos[aleatorio], precios[aleatorio]] # Crea una sublista de 2 posiciones
print("Modelo: " + coche[0] + " Precio:" + coche[1]) # Acceso por índice [0] y [1]