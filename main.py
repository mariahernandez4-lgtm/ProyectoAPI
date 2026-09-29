"""Punto de entrada de la aplicación.
Coordina el módulo ui (entrada/salida) con el módulo api (datos).
"""
from api import consultar_casos
from ui import pedir_datos, mostrar_resultados, mostrar_mensaje


def main():
    while True:
        departamento, limite = pedir_datos()
        mostrar_mensaje("\nConsultando la API, espere un momento...")
        try:
            df = consultar_casos(departamento, limite)
        except ConnectionError as error:
            mostrar_mensaje(f"\nError: {error}")
        else:
            mostrar_resultados(df)

        otra = input("\n¿Desea hacer otra consulta? (s/n): ").strip().lower()
        if otra != "s":
            mostrar_mensaje("Hasta luego.")
            break


if __name__ == "__main__":
    main()
