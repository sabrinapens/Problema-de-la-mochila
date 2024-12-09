# Datos de entrada
costos_facebook = [200, 300, 250, 400, 150, 350, 220, 250, 180, 320]
impactos_facebook = [300, 500, 450, 650, 250, 550, 400, 350, 300, 600]

costos_google = [250, 350, 300, 450, 200, 400, 280, 300, 230, 370]#costo por publicar un anuncio
impactos_google = [350, 600, 550, 750, 300, 650, 450, 500, 350, 700]#beneficio o personas alcanzadas por cada tipo de anuncio

presupuesto_facebook = 1000
presupuesto_google = 1200

n = len(costos_facebook)#En este caso, len es 10

# Inicializar matriz de programación dinámica, tridimensional
dp = [[[0, set()] for _ in range(presupuesto_google + 1)] for _ in range(presupuesto_facebook + 1)]

# Llenar la matriz dp para ambas plataformas
for i in range(n):
    for f in range(presupuesto_facebook, costos_facebook[i] - 1, -1):
        for g in range(presupuesto_google, costos_google[i] - 1, -1):
            # Caso en el que el anuncio se asigna a Facebook
            if f - costos_facebook[i] >= 0:
                #si hay suficiente presupuesto: Calculamos el nuevo impacto, como el impacto anterior más el impacto de este anuncio. 
                #actualizamos dp[f][g][0] si este impacto es mayor que el actual. Guardamos los anuncios asignados en dp[f][g][1]
                valor_facebook = dp[f - costos_facebook[i]][g][0] + impactos_facebook[i]
                if valor_facebook > dp[f][g][0]:
                    dp[f][g][0] = valor_facebook
                    dp[f][g][1] = dp[f - costos_facebook[i]][g][1].copy()
                    dp[f][g][1].add((i, 'Facebook'))
            # Caso en el que el anuncio se asigna a Google
            if g - costos_google[i] >= 0:
                valor_google = dp[f][g - costos_google[i]][0] + impactos_google[i]
                if valor_google > dp[f][g][0]:
                    dp[f][g][0] = valor_google
                    dp[f][g][1] = dp[f][g - costos_google[i]][1].copy()
                    dp[f][g][1].add((i, 'Google'))

# Resultados
valor_maximo = dp[presupuesto_facebook][presupuesto_google][0]
asignaciones = dp[presupuesto_facebook][presupuesto_google][1]

# Separar anuncios por plataforma
anuncios_facebook = {i for i, plataforma in asignaciones if plataforma == 'Facebook'}
anuncios_google = {i for i, plataforma in asignaciones if plataforma == 'Google'}
anuncios_no_incluidos = set(range(n)) - anuncios_facebook - anuncios_google

# Imprimir resultados
print("Valor máximo de ventas:", valor_maximo)
print("Anuncios asignados a Facebook:", anuncios_facebook)
print("Anuncios asignados a Google:", anuncios_google)
print("Anuncios no incluidos en ninguna plataforma:", anuncios_no_incluidos)
