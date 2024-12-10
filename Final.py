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
    predecesor = np.zeros((n + 1, presupuesto_facebook + 1, presupuesto_google + 1), dtype=int)

    # Llenar el tensor Bopt con programación dinámica
    for i in range(1, n + 1):
        for w1 in range(presupuesto_facebook + 1):
            for w2 in range(presupuesto_google + 1):
                # Caso de exclusión del elemento
                Bopt[i][w1][w2] = Bopt[i - 1][w1][w2]
                predecesor[i][w1][w2] = 0  # Se excluye el anuncio por defecto

                # Caso de inclusión en Facebook
                if w1 >= costos_facebook[i - 1]:
                    beneficio_facebook = Bopt[i - 1][w1 - costos_facebook[i - 1]][w2] + impactos_facebook[i - 1]
                    if beneficio_facebook > Bopt[i][w1][w2]:
                        Bopt[i][w1][w2] = beneficio_facebook
                        predecesor[i][w1][w2] = 1  # Se incluye el anuncio en Facebook

                # Caso de inclusión en Google
                if w2 >= costos_google[i - 1]:
                    beneficio_google = Bopt[i - 1][w1][w2 - costos_google[i - 1]] + impactos_google[i - 1]
                    if beneficio_google > Bopt[i][w1][w2]:
                        Bopt[i][w1][w2] = beneficio_google
                        predecesor[i][w1][w2] = 2  # Se incluye el anuncio en Google

    # Recuperar los anuncios asignados con presupuesto
    valor_maximo = Bopt[n][presupuesto_facebook][presupuesto_google]
    anuncios_facebook = set()
    anuncios_google = set()
    valor_facebook = 0
    valor_google = 0

    i, w1, w2 = n, presupuesto_facebook, presupuesto_google
    while i > 0:
        if predecesor[i][w1][w2] == 0:
            i -= 1  # Anuncio no incluido
        elif predecesor[i][w1][w2] == 1:
            anuncios_facebook.add(i - 1)  # Anuncio incluido en Facebook
            valor_facebook += impactos_facebook[i - 1]
            i, w1 = i - 1, w1 - costos_facebook[i - 1]
        elif predecesor[i][w1][w2] == 2:
            anuncios_google.add(i - 1)  # Anuncio incluido en Google
            valor_google += impactos_google[i - 1]
            i, w2 = i - 1, w2 - costos_google[i - 1]

    anuncios_incluidos = anuncios_facebook.union(anuncios_google)
    anuncios_no_incluidos = set(range(n)) - anuncios_incluidos

    return valor_maximo, valor_facebook, valor_google, anuncios_facebook, anuncios_google, anuncios_no_incluidos

# Uso de la función mochila
valor_maximo, valor_facebook, valor_google, anuncios_facebook, anuncios_google, anuncios_no_incluidos = mochila(
    costos_facebook, impactos_facebook, costos_google, impactos_google, presupuesto_facebook, presupuesto_google
)

print("Valor máximo de ventas con presupuesto:", valor_maximo)
print("Valor de ventas submochila Facebook:", valor_facebook)
print("Valor de ventas submochila Google:", valor_google)
print("Anuncios asignados a Facebook con presupuesto:", anuncios_facebook)
print("Anuncios asignados a Google con presupuesto:", anuncios_google)
print("Anuncios no incluidos en ninguna plataforma con presupuesto:", anuncios_no_incluidos)

# Modificación similar para maximizar_sin_presupuesto
# Normalización de los impactos
factor_reduccion = 10
impactos_facebook = [i // factor_reduccion for i in impactos_facebook]
impactos_google = [i // factor_reduccion for i in impactos_google]

max_impacto_facebook = sum(impactos_facebook)
max_impacto_google = sum(impactos_google)

def maximizar_sin_presupuesto(impactos_facebook, impactos_google):
    n = len(impactos_facebook)
    dp = np.zeros((2, max_impacto_facebook + 1, max_impacto_google + 1))

    # Procesa cada fila en paralelo
    def compute_row(i, f_start, f_end):
        temp_row = np.zeros((f_end - f_start, max_impacto_google + 1))
        for f in range(f_start, f_end):
            for g in range(max_impacto_google + 1):
                value = dp[(i - 1) % 2][f][g]
                if f >= impactos_facebook[i - 1]:
                    value = max(value, dp[(i - 1) % 2][f - impactos_facebook[i - 1]][g] + impactos_facebook[i - 1])
                if g >= impactos_google[i - 1]:
                    value = max(value, dp[(i - 1) % 2][f][g - impactos_google[i - 1]] + impactos_google[i - 1])
                temp_row[f - f_start][g] = value
        return temp_row

    for i in range(1, n + 1):
        step = max_impacto_facebook // 4
        ranges = [(start, min(start + step, max_impacto_facebook + 1)) for start in range(0, max_impacto_facebook + 1, step)]
        results = Parallel(n_jobs=-1)(
            delayed(compute_row)(i, start, end) for start, end in ranges
        )
        dp[i % 2] = np.vstack(results)

    # Recuperar el valor máximo
    valor_maximo = int(dp[n % 2].max()) * factor_reduccion

    # Recuperar los anuncios seleccionados
    anuncios_facebook = []
    anuncios_google = []
    valor_facebook = 0
    valor_google = 0
    impacto_f = np.where(dp[n % 2] == dp[n % 2].max())[0][0]
    impacto_g = np.where(dp[n % 2][impacto_f] == dp[n % 2].max())[0][0]

    for i in range(n, 0, -1):
        if impacto_f >= impactos_facebook[i - 1] and dp[i % 2][impacto_f][impacto_g] == dp[(i - 1) % 2][impacto_f - impactos_facebook[i - 1]][impacto_g] + impactos_facebook[i - 1]:
            anuncios_facebook.append(i - 1)
            valor_facebook += impactos_facebook[i - 1] * factor_reduccion
            impacto_f -= impactos_facebook[i - 1]
        elif impacto_g >= impactos_google[i - 1] and dp[i % 2][impacto_f][impacto_g] == dp[(i - 1) % 2][impacto_f][impacto_g - impactos_google[i - 1]] + impactos_google[i - 1]:
            anuncios_google.append(i - 1)
            valor_google += impactos_google[i - 1] * factor_reduccion
            impacto_g -= impactos_google[i - 1]

    anuncios_facebook = np.array(anuncios_facebook)
    anuncios_google = np.array(anuncios_google)
    anuncios_incluidos = set(anuncios_facebook).union(set(anuncios_google))
    anuncios_no_incluidos = set(range(n)) - anuncios_incluidos

    return valor_maximo, valor_facebook, valor_google, anuncios_facebook, anuncios_google, anuncios_no_incluidos

# Ejecutar el cálculo sin presupuesto
valor_maximo_sin_presupuesto, valor_facebook_sin_presupuesto, valor_google_sin_presupuesto, anuncios_facebook_sin_presupuesto, anuncios_google_sin_presupuesto, anuncios_no_incluidos = maximizar_sin_presupuesto(
    impactos_facebook, impactos_google
)

print("Valor máximo de ventas sin presupuesto:", valor_maximo_sin_presupuesto)
print("Valor de ventas submochila Facebook sin presupuesto:", valor_facebook_sin_presupuesto)
print("Valor de ventas submochila Google sin presupuesto:", valor_google_sin_presupuesto)
print("Anuncios asignados a Facebook sin presupuesto:", anuncios_facebook_sin_presupuesto)
print("Anuncios asignados a Google sin presupuesto:", anuncios_google_sin_presupuesto)
print("Anuncios no incluidos en ninguna plataforma sin presupuesto:", anuncios_no_incluidos)
