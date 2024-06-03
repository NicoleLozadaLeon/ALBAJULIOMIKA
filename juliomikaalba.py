import streamlit as st
import pandas as pd
import altair as alt

def obtener_monto():
    while True:
        try:
            monto = float(input("Ingrese el monto para el cual quiere realizar el plan de gastos mensual en bolivianos (Bs): "))
            if monto > 0:
                return monto
            else:
                print("Por favor, ingrese un monto positivo.")
        except ValueError:
            print("Por favor, ingrese un número válido.")

def obtener_porcentaje_ahorro():
    while True:
        porcentaje = input("¿Cuánto quiere ahorrar? (0%, 3%, 6%, 9%): ").strip()
        if porcentaje in ["0", "3", "6", "9"]:
            return float(porcentaje.strip('%')) / 100
        else:
            print("Por favor, seleccione un porcentaje válido (0, 3, 6, 9)")

def pregunta_si_no(mensaje):
    while True:
        respuesta = input(mensaje + " (si o no): ").strip().lower()
        if respuesta == "si":
            return True
        elif respuesta == "no":
            return False
        else:
            print("Por favor, responda con 'si' o 'no'.")

def obtener_gasto_si_no(mensaje):
    if pregunta_si_no(mensaje):
        while True:
            try:
                gasto = float(input("¿Cuánto paga? "))
                if gasto >= 0:
                    return gasto
                else:
                    print("Por favor, ingrese un monto positivo.")
            except ValueError:
                print("Por favor, ingrese un número válido.")
    else:
        return 0

def seleccionar_categorias():
    categorias = ["ALIMENTACION", "SERVICIOS BASICOS", "TRANSPORTE", "OCIO", "COMUNICACION", "SALUD"]
    seleccionadas = []
    for categoria in categorias:
        if pregunta_si_no(f"¿Tiene gasto en la categoría {categoria}?"):
            seleccionadas.append(categoria)
    return seleccionadas

def prioridad_categorias(seleccionadas):
    prioridades = {}
    for i, categoria in enumerate(seleccionadas):
        while True:
            try:
                prioridad = int(input(f"Asignar prioridad a {categoria} (1 para la más importante, {len(seleccionadas)} para la menos importante): "))
                if 1 <= prioridad <= len(seleccionadas) and prioridad not in prioridades.values():
                    prioridades[categoria] = prioridad
                    break
                else:
                    print("Por favor, ingrese una prioridad válida y no repetida.")
            except ValueError:
                print("Por favor, ingrese un número válido.")
    return prioridades

def calcular_porcentajes(prioridades):
    n = len(prioridades)
    porcentaje_categoria = {
        1: {1: 100},
        2: {1: 60, 2: 40},
        3: {1: 45, 2: 30, 3: 25},
        4: {1: 32, 2: 27, 3: 23, 4: 18},
        5: {1: 30, 2: 25, 3: 20, 4: 15, 5: 10},
        6: {1: 26, 2: 22, 3: 19, 4: 15, 5: 11, 6: 7}
    }
    return {categoria: porcentaje_categoria[n][prioridad] / 100 for categoria, prioridad in prioridades.items()}

def calcular_subcategorias(categoria):
    subcategorias = []
    if categoria == "SERVICIOS BASICOS":
        subcategorias = ["LUZ", "AGUA", "GAS"]
    elif categoria == "COMUNICACION":
        subcategorias = ["CREDITO", "INTERNET"]

    prioridades = {}
    for subcategoria in subcategorias:
        while True:
            try:
                prioridad = int(input(f"Asignar prioridad a {subcategoria} (1 para la más importante, {len(subcategorias)} para la menos importante): "))
                if 1 <= prioridad <= len(subcategorias) and prioridad not in prioridades.values():
                    prioridades[subcategoria] = prioridad
                    break
                else:
                    print("Por favor, ingrese una prioridad válida y no repetida.")
            except ValueError:
                print("Por favor, ingrese un número válido.")

    n = len(prioridades)
    porcentaje_subcategoria = {
        1: {1: 100},
        2: {1: 60, 2: 40},
        3: {1: 45, 2: 30, 3: 25}
    }
    return {subcategoria: porcentaje_subcategoria[n][prioridad] / 100 for subcategoria, prioridad in prioridades.items()}

def main():
    monto = obtener_monto()
    porcentaje_ahorro = obtener_porcentaje_ahorro()
    ahorro = monto * porcentaje_ahorro

    alquiler = obtener_gasto_si_no("¿Paga alquiler?")
    deudas = obtener_gasto_si_no("¿Tiene deudas económicas o educativas? Por ejemplo, deudas bancarias o cuotas del colegio/universidad")
    actividades = obtener_gasto_si_no("¿Realiza actividades extracurriculares como gimnasio, danza, ajedrez, etc?")

    total_1 = monto - alquiler - deudas - actividades
    total_2 = total_1 * porcentaje_ahorro
    total_final = total_1 - total_2

    seleccionadas = seleccionar_categorias()
    prioridades = prioridad_categorias(seleccionadas)
    porcentajes = calcular_porcentajes(prioridades)

    resultados = {}
    for categoria, porcentaje in porcentajes.items():
        if categoria in ["SERVICIOS BASICOS", "COMUNICACION"]:
            subcategorias = calcular_subcategorias(categoria)
            resultados[categoria] = {subcategoria: total_final * porcentaje * porcentaje_subcategoria for subcategoria, porcentaje_subcategoria in subcategorias.items()}
        else:
            resultados[categoria] = total_final * porcentaje

    resultados["AHORRO"] = ahorro
    resultados["ALQUILER"] = alquiler
    resultados["ACTIVIDADES EXTRACURRICULARES"] = actividades
    resultados["DEUDAS"] = deudas

    print("\nEste sería tu plan de gastos mensual si quisieras ahorrar: ", porcentaje_ahorro, "%")
    for categoria, valor in resultados.items():
        if isinstance(valor, dict):
            print(f"{categoria}:")
            for subcategoria, subvalor in valor.items():
                print(f"  {subcategoria}: {subvalor:.2f} Bs")
        else:
            print(f"{categoria}: {valor:.2f} Bs")

if __name__ == "__main__":
    main()
