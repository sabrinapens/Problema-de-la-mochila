import numpy as np
from graphviz import Digraph

# Datos de entrada
costos_facebook = [200, 300, 250, 400, 150, 350, 220, 250, 180, 320]
impactos_facebook = [300, 500, 450, 650, 250, 550, 400, 350, 300, 600]
costos_google = [250, 350, 300, 450, 200, 400, 280, 300, 230, 370]
impactos_google = [350, 600, 550, 750, 300, 650, 450, 500, 350, 700]
presupuesto_facebook = 1000
presupuesto_google = 1200


# Mochila con restricciones de presupuesto
def mochila_con_presupuesto(costos_facebook, impactos_facebook, costos_google, impactos_google, presupuesto_facebook,
                            presupuesto_google):
    cantidad_anuncios = len(costos_facebook)
    beneficios_optimos = np.zeros((cantidad_anuncios + 1, presupuesto_facebook + 1, presupuesto_google + 1))
    predecesor = np.zeros((cantidad_anuncios + 1, presupuesto_facebook + 1, presupuesto_google + 1), dtype=int)

    for i in range(1, cantidad_anuncios + 1):
        for presupuesto_fb in range(presupuesto_facebook + 1):
            for presupuesto_gg in range(presupuesto_google + 1):
                beneficios_optimos[i][presupuesto_fb][presupuesto_gg] = beneficios_optimos[i - 1][presupuesto_fb][
                    presupuesto_gg]
                predecesor[i][presupuesto_fb][presupuesto_gg] = 0

                if presupuesto_fb >= costos_facebook[i - 1]:
                    beneficio_fb = beneficios_optimos[i - 1][presupuesto_fb - costos_facebook[i - 1]][presupuesto_gg] + \
                                   impactos_facebook[i - 1]
                    if beneficio_fb > beneficios_optimos[i][presupuesto_fb][presupuesto_gg]:
                        beneficios_optimos[i][presupuesto_fb][presupuesto_gg] = beneficio_fb
                        predecesor[i][presupuesto_fb][presupuesto_gg] = 1

                if presupuesto_gg >= costos_google[i - 1]:
                    beneficio_gg = beneficios_optimos[i - 1][presupuesto_fb][presupuesto_gg - costos_google[i - 1]] + \
                                   impactos_google[i - 1]
                    if beneficio_gg > beneficios_optimos[i][presupuesto_fb][presupuesto_gg]:
                        beneficios_optimos[i][presupuesto_fb][presupuesto_gg] = beneficio_gg
                        predecesor[i][presupuesto_fb][presupuesto_gg] = 2

    valor_maximo = beneficios_optimos[cantidad_anuncios][presupuesto_facebook][presupuesto_google]
    return valor_maximo, predecesor


# Maximización sin restricciones
def maximizar_sin_restricciones(impactos_facebook, impactos_google):
    cantidad_anuncios = len(impactos_facebook)
    dp = [0] * (cantidad_anuncios + 1)
    predecesor = np.zeros((cantidad_anuncios + 1, 2), dtype=int)  # 0: Facebook, 1: Google

    for i in range(1, cantidad_anuncios + 1):
        if impactos_facebook[i - 1] >= impactos_google[i - 1]:
            dp[i] = dp[i - 1] + impactos_facebook[i - 1]
            predecesor[i][0] = 1  # Seleccionado en Facebook
        else:
            dp[i] = dp[i - 1] + impactos_google[i - 1]
            predecesor[i][1] = 1  # Seleccionado en Google

    valor_maximo = dp[cantidad_anuncios]
    return valor_maximo, predecesor


# Función para obtener los anuncios asignados y excluidos
def obtener_anuncios(predecesor, costos_facebook, costos_google, presupuesto_facebook, presupuesto_google):
    cantidad_anuncios = len(costos_facebook)
    anuncios_fb = []
    anuncios_gg = []
    anuncios_no_incluidos = []
    valor_fb = 0
    valor_gg = 0

    for i in range(cantidad_anuncios, 0, -1):
        if predecesor[i][presupuesto_facebook][presupuesto_google] == 1:  # Anuncio asignado a Facebook
            anuncios_fb.append(i - 1)
            valor_fb += impactos_facebook[i - 1]
            presupuesto_facebook -= costos_facebook[i - 1]
        elif predecesor[i][presupuesto_facebook][presupuesto_google] == 2:  # Anuncio asignado a Google
            anuncios_gg.append(i - 1)
            valor_gg += impactos_google[i - 1]
            presupuesto_google -= costos_google[i - 1]
        else:
            anuncios_no_incluidos.append(i - 1)

    return anuncios_fb, anuncios_gg, anuncios_no_incluidos, valor_fb, valor_gg


# Generar el diagrama de decisiones para la función mochila
def generar_diagrama_mochila(predecesor, costos_facebook, costos_google, cantidad_anuncios, presupuesto_fb, presupuesto_gg):
    diagrama = Digraph(comment='Árbol de decisiones - Mochila con presupuesto')
    pila = [(cantidad_anuncios, presupuesto_fb, presupuesto_gg)]
    visitados = set()

    while pila:
        i, presupuesto_fb, presupuesto_gg = pila.pop()
        if (i, presupuesto_fb, presupuesto_gg) in visitados:
            continue
        visitados.add((i, presupuesto_fb, presupuesto_gg))

        if i == 0:
            diagrama.node(f"0,{presupuesto_fb},{presupuesto_gg}", f"Estado inicial: ({presupuesto_fb}, {presupuesto_gg})")
        else:
            etiqueta_padre = f"{i},{presupuesto_fb},{presupuesto_gg}"
            diagrama.node(etiqueta_padre, f"Anuncio {i - 1}: ({presupuesto_fb}, {presupuesto_gg})")
            if predecesor[i][presupuesto_fb][presupuesto_gg] == 0:
                pila.append((i - 1, presupuesto_fb, presupuesto_gg))
                diagrama.edge(etiqueta_padre, f"{i - 1},{presupuesto_fb},{presupuesto_gg}", "Excluir")
            elif predecesor[i][presupuesto_fb][presupuesto_gg] == 1:
                pila.append((i - 1, presupuesto_fb - costos_facebook[i - 1], presupuesto_gg))
                diagrama.edge(etiqueta_padre, f"{i - 1},{presupuesto_fb - costos_facebook[i - 1]},{presupuesto_gg}",
                              "Facebook")
            elif predecesor[i][presupuesto_fb][presupuesto_gg] == 2:
                pila.append((i - 1, presupuesto_fb, presupuesto_gg - costos_google[i - 1]))
                diagrama.edge(etiqueta_padre, f"{i - 1},{presupuesto_fb},{presupuesto_gg - costos_google[i - 1]}",
                              "Google")

    return diagrama


# Generar el diagrama de decisiones para la función sin presupuesto
def generar_diagrama_sin_restricciones(predecesor, cantidad_anuncios):
    diagrama = Digraph(comment='Árbol de decisiones - Sin restricciones')
    pila = [cantidad_anuncios]
    visitados = set()

    while pila:
        i = pila.pop()
        if i in visitados:
            continue
        visitados.add(i)

        etiqueta_padre = f"Anuncio {i - 1}"
        diagrama.node(etiqueta_padre, etiqueta_padre)
        if i == 0:
            diagrama.node("Inicio", "Inicio")
            diagrama.edge("Inicio", etiqueta_padre)
        else:
            if predecesor[i][0] == 1:  # Facebook
                pila.append(i - 1)
                diagrama.edge(etiqueta_padre, f"Anuncio {i - 2}", "Facebook")
            elif predecesor[i][1] == 1:  # Google
                pila.append(i - 1)
                diagrama.edge(etiqueta_padre, f"Anuncio {i - 2}", "Google")

    return diagrama


# Ejecutar las funciones
valor_maximo, predecesor = mochila_con_presupuesto(
    costos_facebook, impactos_facebook, costos_google, impactos_google, presupuesto_facebook, presupuesto_google)
anuncios_fb, anuncios_gg, anuncios_no_incluidos, valor_fb, valor_gg = obtener_anuncios(
    predecesor, costos_facebook, costos_google, presupuesto_facebook, presupuesto_google)

valor_maximo_sin_presupuesto, predecesor_sin_presupuesto = maximizar_sin_restricciones(
    impactos_facebook, impactos_google)

# Mostrar los resultados de la maximización con presupuesto
print("\n=== Mochila con presupuesto ===")
print(f"Valor máximo total con presupuesto: {valor_maximo}")
print(f"Valor Facebook con presupuesto: {valor_fb}, Anuncios Facebook: {anuncios_fb}")
print(f"Valor Google con presupuesto: {valor_gg}, Anuncios Google: {anuncios_gg}")
print(f"Anuncios no incluidos en ninguna plataforma: {anuncios_no_incluidos}")

# Mostrar los resultados de la maximización sin restricciones
print("\n=== Maximización sin restricciones ===")
print(f"Valor máximo total sin presupuesto: {valor_maximo_sin_presupuesto}")
print(f"Anuncios asignados a Facebook sin presupuesto: {anuncios_fb}")
print(f"Anuncios asignados a Google sin presupuesto: {anuncios_gg}")

# Generar y guardar el diagrama de decisiones con presupuesto
diagrama_con_presupuesto = generar_diagrama_mochila(predecesor, costos_facebook, costos_google, len(costos_facebook),
                                                    presupuesto_facebook, presupuesto_google)
diagrama_con_presupuesto.render("arbol_mochila", format="png", cleanup=True)
print("\nDiagrama de decisiones con presupuesto guardado como 'arbol_mochila.png'.")

# Generar y guardar el diagrama de decisiones sin restricciones
diagrama_sin_restricciones = generar_diagrama_sin_restricciones(predecesor_sin_presupuesto, len(impactos_facebook))
diagrama_sin_restricciones.render("arbol_sin_restricciones", format="png", cleanup=True)
print("Diagrama de decisiones sin restricciones guardado como 'arbol_sin_restricciones.png'.")
