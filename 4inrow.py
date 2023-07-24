import os

# Definir variables de color
AMARILLO = "\033[93m"
BLANCO = "\033[97m"
VERDE = "\033[92m"
ROJO = "\033[91m"
RESET = "\033[0m"


def cabecera():
    print(ROJO + title + RESET)
    print(divider)


title = """
██╗  ██╗    ██╗███╗   ██╗    ██████╗  ██████╗ ██╗    ██╗
██║  ██║    ██║████╗  ██║    ██╔══██╗██╔═══██╗██║    ██║
███████║    ██║██╔██╗ ██║    ██████╔╝██║   ██║██║ █╗ ██║
╚════██║    ██║██║╚██╗██║    ██╔══██╗██║   ██║██║███╗██║
     ██║    ██║██║ ╚████║    ██║  ██║╚██████╔╝╚███╔███╔╝
     ╚═╝    ╚═╝╚═╝  ╚═══╝    ╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝                                                   
< afsh4ck >"""

divider = "-------------------------------------------"


def crear_tablero(filas, columnas):
    tablero = [["."] * columnas for _ in range(filas)]
    return tablero


def mostrar_tablero(tablero, ganador=None):
    # Limpia la pantalla dependiendo del sistema operativo
    if os.name == 'nt':
        os.system('cls')  # Windows
    else:
        os.system('clear')  # Linux / macOS

    # Imprimimos la cabecera
    cabecera()

    # Imprimimos los números de columna
    print(" ", end=" ")
    for num in range(len(tablero[0])):
        print(num, end="  ")
    print()

    # Imprimimos el tablero con las fichas
    for fila_idx, fila in enumerate(tablero):
        print("|", end=" ")
        for col_idx, casilla in enumerate(fila):
            if ganador and (fila_idx, col_idx) in ganador:
                print(VERDE + casilla + RESET, end="  ")
            else:
                print(casilla, end="  ")
        print("|")
    print(divider)


def validar_columna(tablero, columna):
    return 0 <= columna < len(tablero[0])


def columna_llena(tablero, columna):
    return tablero[0][columna] != '.'


def introducir_ficha(tablero, columna, color):
    if not validar_columna(tablero, columna):
        print(ROJO + "[!] ERROR: Número de columna fuera del rango" + RESET)
        return False
    if columna_llena(tablero, columna):
        print(ROJO + "[!] ERROR: La columna está llena de fichas" + RESET)
        return False

    for fila in range(len(tablero) - 1, -1, -1):
        if tablero[fila][columna] == '.':
            tablero[fila][columna] = color
            return True


def revisar_filas(tablero, color):
    for fila in tablero:
        for c in range(len(tablero[0]) - 3):
            if all(casilla == color for casilla in fila[c:c + 4]):
                return [(i, c + i) for i in range(4)]
    return []


def revisar_columnas(tablero, color):
    for c in range(len(tablero[0])):
        for r in range(len(tablero) - 3):
            if all(tablero[r + i][c] == color for i in range(4)):
                return [(r + i, c) for i in range(4)]
    return []


def revisar_diagonales(tablero, color):
    for r in range(len(tablero) - 3):
        for c in range(len(tablero[0])):
            if c <= len(tablero[0]) - 4:
                # Diagonal derecha \
                if all(tablero[r + i][c + i] == color for i in range(4)):
                    return [(r + i, c + i) for i in range(4)]
            if c >= 3:
                # Diagonal izquierda /
                if all(tablero[r + i][c - i] == color for i in range(4)):
                    return [(r + i, c - i) for i in range(4)]
    return []


def comprobar_ganador(tablero, color):
    return (
            revisar_filas(tablero, color) or
            revisar_columnas(tablero, color) or
            revisar_diagonales(tablero, color)
    )


def juego_cuatro_en_raya():
    tablero = crear_tablero(6, 7)
    jugadores = [("X", "Jugador X"), ("O", "Jugador O")]
    turno_actual = 0

    while True:
        color, nombre = jugadores[turno_actual]
        mostrar_tablero(tablero)
        columna = input(f"Turno del {nombre}: ")

        if not columna.isdigit():
            print(ROJO + "[!] ERROR: Debes ingresar un número de columna válido." + RESET)
            continue

        columna = int(columna)
        if not introducir_ficha(tablero, columna, color):
            continue

        ganador = comprobar_ganador(tablero, color)
        if ganador:
            mostrar_tablero(tablero, ganador)
            print(f"{VERDE}[+] ¡Ha ganado el {nombre}!{RESET}\n\n")
            break

        if all(all(casilla != '.' for casilla in fila) for fila in tablero):
            mostrar_tablero(tablero)
            print(AMARILLO + "[!] ¡Empate! No hay más movimientos posibles.\n\n" + RESET)
            break

        turno_actual = (turno_actual + 1) % 2


juego_cuatro_en_raya()