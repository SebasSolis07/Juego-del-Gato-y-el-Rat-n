# Función para crear la matriz del tablero
def crear_tablero(dim):
    tablero = []
    for i in range(dim):
        fila = []
        for j in range(dim):
            fila.append('.')  # Inicializamos con puntos cada celda
        tablero.append(fila)  # Cargo un vector dentro de otro vector
    return tablero  # Envio la matriz cargada a la función

# Función para mostrar el tablero en pantalla
def mostrar_tablero(posicion_gato, posicion_raton, dim, meta):
    tablero = crear_tablero(dim)  # Se crea la matriz y se retorna

    # Reemplazo los puntos por caracteres que representan a R=ratón, G=gato, Q=queso/meta
    tablero[meta[0]][meta[1]] = 'Q'  # Meta del ratón
    tablero[posicion_gato[0]][posicion_gato[1]] = 'G'  # Posición del gato
    tablero[posicion_raton[0]][posicion_raton[1]] = 'R'  # Posición del ratón

    # Imprimo la matriz actualizada
    for i in range(dim):
        for j in range(dim):
            print(tablero[i][j], end=' ')
        print()  # Salto de línea al final de cada fila

# Función que permite que el usuario mueva al ratón
def movimiento_usuario(posicion_raton, dim):
    print("Movimientos con el teclado: w/a/s/d")
    tecla = input("Movimiento: ").lower()  # Convertir a minúscula

    nueva_fila = posicion_raton[0]
    nueva_columna = posicion_raton[1]

    # Condiciones de movimiento dentro de la matriz
    if tecla == "w" and nueva_fila > 0:
        nueva_fila -= 1
    elif tecla == "s" and nueva_fila < dim - 1:
        nueva_fila += 1
    elif tecla == "a" and nueva_columna > 0:
        nueva_columna -= 1
    elif tecla == "d" and nueva_columna < dim - 1:
        nueva_columna += 1

    return [nueva_fila, nueva_columna]  # Retorno la nueva posición

# Función para calcular la distancia Manhattan entre ratón y gato
def distancia_manhattan(posicion_raton, posicion_gato):
    return abs(posicion_raton[0] - posicion_gato[0]) + abs(posicion_raton[1] - posicion_gato[1])

# Función que devuelve todos los movimientos posibles del gato en la matriz
def movimientos_gato(posicion, dimension):
    fila = posicion[0]
    columna = posicion[1]
    lista = []

    if fila > 0:
        lista.append([fila - 1, columna])
    if fila < dimension - 1:
        lista.append([fila + 1, columna])
    if columna > 0:
        lista.append([fila, columna - 1])
    if columna < dimension - 1:
        lista.append([fila, columna + 1])
    return lista


# Función minimax para que el gato decida su movimiento
# turno_gato = True -> es turno del gato
# turno_gato = False -> se simula movimiento del ratón
# La profundidad para mi representa las ramas       
def minimax(posicion_gato, posicion_raton, dim, profundidad, turno_gato):
    # No mira movimiento  o  el gato atrapó al ratón
    if profundidad == 0 or posicion_gato == posicion_raton:
        valor = distancia_manhattan(posicion_raton, posicion_gato)
        return valor, posicion_gato[:]

    # Despues del movimiento del raton ahora es el movimiento del gato
    if turno_gato:
        
        mejor_valor = 9999
        mejor_movimiento = posicion_gato[:]
        lista_movimientos = movimientos_gato(posicion_gato, dim)

            
        for mov in lista_movimientos:
            nuevo_gato=[mov[0],mov[1]]
            valor,datoextra = minimax(nuevo_gato, [posicion_raton[0], posicion_raton[1]], dim, profundidad - 1, False)
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_movimiento = [mov[0], mov[1]]
        return mejor_valor, mejor_movimiento
    else:
        # Turno del ratón: simulo movimientos posibles
        mejor_valor = -9999
        mejor_movimiento = posicion_raton[:]
        lista_movimientos = movimientos_gato(posicion_raton, dim)
        for mov in lista_movimientos:
            valor, _ = minimax(posicion_gato, mov, dim, profundidad - 1, True)
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = mov
        return mejor_valor, mejor_movimiento



# Función principal que inicia el juego
def empezar():

    dim = 5  # Dimension de la matriz cuadrada
    posicion_gato = [0, 0]  # Posición inicial del gato
    posicion_raton = [4, 0]  # Posición inicial del ratón
    meta = [0, dim - 1]  # Meta de salida del ratón
    turnos = 1 #Acumulador de turnos 
     
    while turnos < 10: #Hasta 10 turnos 
        # Mostrar tablero
        mostrar_tablero(posicion_gato, posicion_raton, dim, meta)

        # Condición de fin si el gato atrapa al ratón
        if posicion_gato == posicion_raton:
            print("El gato atrapó al ratón")
            break
        # Condicion de fin si el gato llega a la Q 
        if posicion_raton == meta :
            print ('Ganaste')
            break 

        # Movimiento del ratón por el usuario
        posicion_raton = movimiento_usuario(posicion_raton, dim)
        if posicion_raton == posicion_gato:
            print("El gato atrapó al ratón")
            break

        # Definido del movimiento del rato pasamos al minimax. El gato va analizar ciertas coordenas 
        valor, mejor_movimiento_gato = minimax(posicion_gato, posicion_raton, dim, 1, True)
        posicion_gato = mejor_movimiento_gato[:]  # Actualizamos posición del gato
        turnos = turnos +1 # Limitar la cantidad de turnos para liquidar mas rapido el juego 


# Llamada al programa principal
empezar()
