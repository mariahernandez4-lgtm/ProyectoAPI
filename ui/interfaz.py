"""Interfaz de usuario por consola.
Solo pide datos y muestra resultados; NO consulta la API.
"""
LIMITE_MAXIMO = 500  # evita que la consulta se "cuelgue"

ENCABEZADO = "{:<22} {:<16} {:>5}  {:<20} {:<12} {:<20}"
FILA = "{:<22.22} {:<16.16} {:>5}  {:<20.20} {:<12.12} {:<20.20}"


def mostrar_mensaje(texto):
    print(texto)


def pedir_datos():
    """Pide departamento y número de registros. Devuelve (str, int)."""
    print("=" * 60)
    print(" CASOS POSITIVOS DE COVID-19 EN COLOMBIA (datos.gov.co)")
    print("=" * 60)

    while True:
        departamento = input("Departamento a consultar (ej. Risaralda): ").strip()
        if departamento:
            break
        print("  El departamento no puede estar vacío.")

    while True:
        texto = input(f"Número de registros (1-{LIMITE_MAXIMO}): ").strip()
        if texto.isdigit() and 1 <= int(texto) <= LIMITE_MAXIMO:
            return departamento, int(texto)
        print(f"  Ingrese un número entero entre 1 y {LIMITE_MAXIMO}.")


def mostrar_resultados(df):
    """Imprime el DataFrame con formato de tabla usando str.format()."""
    if df.empty:
        print("\nNo se encontraron registros para esa consulta.")
        return

    encabezado = ENCABEZADO.format(*df.columns)
    print("\n" + encabezado)
    print("-" * len(encabezado))
    for fila in df.itertuples(index=False):
        print(FILA.format(*[str(dato) for dato in fila]))
    print("-" * len(encabezado))
    print(f"Total de registros mostrados: {len(df)}")
