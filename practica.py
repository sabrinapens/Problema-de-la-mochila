import numpy as np

# Datos de entrada
costos_facebook = [200, 300, 250, 400, 150, 350, 220, 250, 180, 320]
impactos_facebook = [300, 500, 450, 650, 250, 550, 400, 350, 300, 600]

costos_google = [250, 350, 300, 450, 200, 400, 280, 300, 230, 370]
impactos_google = [350, 600, 550, 750, 300, 650, 450, 500, 350, 700]

presupuesto_facebook = 1000
presupuesto_google = 1200

n = len(costos_facebook)

# Crear tensores Bopt y predecesor
Bopt = np.zeros((n + 1, presupuesto_facebook + 1, presupuesto_google + 1))
predecesor = np.zeros((n + 1, presupuesto_facebook + 1, presupuesto_google + 1), dtype=tuple)

# Llenar el tensor Bopt con programación dinámica
for i in range(1, n + 1):
    for w1 in range(presupuesto_facebook + 1):
        for w2 in range(presupuesto_google + 1):
            # Caso de exclusión del elemento
            Bopt[i][w1][w2] = Bopt[i-1][w1][w2]
            predecesor[i][w1][w2] = (i-1, w1, w2)

            # Caso de inclusión en Facebook
            if w1 >= costos_facebook[i-1]:
                beneficio_facebook = Bopt[i-1][w1 - costos_facebook[i-1]][w2] + impactos_facebook[i-1]
                if beneficio_facebook > Bopt[i][w1][w2]:
                    Bopt[i][w1][w2] = beneficio_facebook
                    predecesor[i][w1][w2] = (i-1, w1 - costos_facebook[i-1], w2)

            # Caso de inclusión en Google
            if w2 >= costos_google[i-1]:
                beneficio_google = Bopt[i-1][w1][w2 - costos_google[i-1]] + impactos_google[i-1]
                if beneficio_google > Bopt[i][w1][w2]:
                    Bopt[i][w1][w2] = beneficio_google
                    predecesor[i][w1][w2] = (i-1, w1, w2 - costos_google[i-1])

# Recuperar los anuncios asignados
valor_maximo = Bopt[n][presupuesto_facebook][presupuesto_google]
anuncios_facebook = set()
anuncios_google = set()

i, w1, w2 = n, presupuesto_facebook, presupuesto_google
while i > 0:
    if predecesor[i][w1][w2] == (i-1, w1, w2):
        # Anuncio no incluido
        i -= 1
    elif predecesor[i][w1][w2] == (i-1, w1 - costos_facebook[i-1], w2):
        # Anuncio incluido en Facebook
        anuncios_facebook.add(i-1)
        i, w1, w2 = i-1, w1 - costos_facebook[i-1], w2
    elif predecesor[i][w1][w2] == (i-1, w1, w2 - costos_google[i-1]):
        # Anuncio incluido en Google
        anuncios_google.add(i-1)
        i, w1, w2 = i-1, w1, w2 - costos_google[i-1]

# Anuncios no incluidos
anuncios_incluidos = anuncios_facebook.union(anuncios_google)
anuncios_no_incluidos = set(range(n)) - anuncios_incluidos

# Imprimir resultados
print("Valor máximo de ventas:", valor_maximo)
print("Anuncios asignados a Facebook:", anuncios_facebook)
print("Anuncios asignados a Google:", anuncios_google)
print("Anuncios no incluidos en ninguna plataforma:", anuncios_no_incluidos)
