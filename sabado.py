import numpy as np
from joblib import Parallel, delayed

# Datos de entrada
costos_facebook = [200, 300, 250, 400, 150, 350, 220, 250, 180, 320]
impactos_facebook = [300, 500, 450, 650, 250, 550, 400, 350, 300, 600]
costos_google = [250, 350, 300, 450, 200, 400, 280, 300, 230, 370]
impactos_google = [350, 600, 550, 750, 300, 650, 450, 500, 350, 700]
presupuesto_facebook = 1000
presupuesto_google = 1200

n = len(costos_facebook)

def mochila(costos_facebook, impactos_facebook, costos_google, impactos_google, presupuesto_facebook, presupuesto_google):
    n = len(costos_facebook)

    # Crear tensores Bopt y predecesor
    Bopt = np.zeros((n + 1, presupuesto_facebook + 1, presupuesto_google + 1))
    predecesor = np.zeros((n + 1, presupuesto_facebook + 1, presupuesto_google + 1), dtype=tuple)

    # Llenar el tensor Bopt con programación dinámica
    for i in range(1, n + 1):
        for w1 in range(presupuesto_facebook + 1):
            for w2 in range(presupuesto_google + 1):
                # Caso de exclusión del elemento
                Bopt[i][w1][w2] = Bopt[i - 1][w1][w2]
                predecesor[i][w1][w2] = (i - 1, w1, w2)

                # Caso de inclusión en Facebook
                if w1 >= costos_facebook[i - 1]:
                    beneficio_facebook = Bopt[i - 1][w1 - costos_facebook[i - 1]][w2] + impactos_facebook[i - 1]
                    if beneficio_facebook > Bopt[i][w1][w2]:
                        Bopt[i][w1][w2] = beneficio_facebook
                        predecesor[i][w1][w2] = (i - 1, w1 - costos_facebook[i - 1], w2)

                # Caso de inclusión en Google
                if w2 >= costos_google[i - 1]:
                    beneficio_google = Bopt[i - 1][w1][w2 - costos_google[i - 1]] + impactos_google[i - 1]
                    if beneficio_google > Bopt[i][w1][w2]:
                        Bopt[i][w1][w2] = beneficio_google
                        predecesor[i][w1][w2] = (i - 1, w1, w2 - costos_google[i - 1])

    # Recuperar los anuncios asignados con presupuesto
    valor_maximo = Bopt[n][presupuesto_facebook][presupuesto_google]
    anuncios_facebook = set()
    anuncios_google = set()

    i, w1, w2 = n, presupuesto_facebook, presupuesto_google
    while i > 0:
        if predecesor[i][w1][w2] == (i - 1, w1, w2):
            i -= 1  # Anuncio no incluido
        elif predecesor[i][w1][w2] == (i - 1, w1 - costos_facebook[i - 1], w2):
            anuncios_facebook.add(i - 1)  # Anuncio incluido en Facebook
            i, w1, w2 = i - 1, w1 - costos_facebook[i - 1], w2
        elif predecesor[i][w1][w2] == (i - 1, w1, w2 - costos_google[i - 1]):
            anuncios_google.add(i - 1)  # Anuncio incluido en Google
            i, w1, w2 = i - 1, w1, w2 - costos_google[i - 1]

    anuncios_incluidos = anuncios_facebook.union(anuncios_google)
    anuncios_no_incluidos = set(range(n)) - anuncios_incluidos

    return valor_maximo, anuncios_facebook, anuncios_google, anuncios_no_incluidos

# Calculamos usando la función `mochila`
valor_maximo, anuncios_facebook, anuncios_google, anuncios_no_incluidos = mochila(
    costos_facebook, impactos_facebook, costos_google, impactos_google, presupuesto_facebook, presupuesto_google
)

print("Valor máximo de ventas con presupuesto:", valor_maximo)
print("Anuncios asignados a Facebook con presupuesto:", anuncios_facebook)
print("Anuncios asignados a Google con presupuesto:", anuncios_google)
print("Anuncios no incluidos en ninguna plataforma con presupuesto:", anuncios_no_incluidos)

# Calcular la venta máxima sin restricciones presupuestarias
memo = {}

def maximizar_sin_presupuesto(i, impactos_facebook, impactos_google, current_impacto_facebook, current_impacto_google):
    if i == n:
        return current_impacto_facebook + current_impacto_google

    if (i, current_impacto_facebook, current_impacto_google) in memo:
        return memo[(i, current_impacto_facebook, current_impacto_google)]

    # Excluir el anuncio
    total_excluido = maximizar_sin_presupuesto(i + 1, impactos_facebook, impactos_google, current_impacto_facebook, current_impacto_google)

    # Incluir el anuncio en Facebook
    total_facebook = maximizar_sin_presupuesto(i + 1, impactos_facebook, impactos_google, current_impacto_facebook + impactos_facebook[i], current_impacto_google)

    # Incluir el anuncio en Google
    total_google = maximizar_sin_presupuesto(i + 1, impactos_facebook, impactos_google, current_impacto_facebook, current_impacto_google + impactos_google[i])

    # Encontrar el máximo de los tres casos
    max_total = max(total_excluido, total_facebook, total_google)

    memo[(i, current_impacto_facebook, current_impacto_google)] = max_total
    return max_total

# Utilizar joblib para paralelizar las llamadas recursivas
resultados = Parallel(n_jobs=-1)(delayed(maximizar_sin_presupuesto)(i, impactos_facebook, impactos_google, 0, 0) for i in range(n))

valor_maximo_sin_presupuesto = max(resultados)

# Imprimir resultados sin restricciones presupuestarias
print("Valor máximo de ventas sin presupuesto:", valor_maximo_sin_presupuesto)
#