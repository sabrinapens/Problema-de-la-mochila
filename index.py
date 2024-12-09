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
    for f in range(presupuesto_facebook, costos_facebook[i] - 1, -1):#Iteramos sobre cada anuncio (i) y cada combinación de presupuestos posibles para Facebook (f) y Google (g).
        for g in range(presupuesto_google, costos_google[i] - 1, -1):
            # Caso en el que el anuncio se asigna a Facebook
            if f - costos_facebook[i] >= 0:
                #si hay suficiente presupuesto: Calculamos el nuevo impacto, como el impacto anterior más el impacto de este anuncio. 
                #actualizamos dp[f][g][0] si este impacto es mayor que el actual. Guardamos los anuncios asignados en dp[f][g][1].
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

# Resultados con presupuesto
valor_maximo_presupuesto = dp[presupuesto_facebook][presupuesto_google][0]
asignaciones_presupuesto = dp[presupuesto_facebook][presupuesto_google][1]

# Separar anuncios por plataforma
anuncios_facebook_presupuesto = {i for i, plataforma in asignaciones_presupuesto if plataforma == 'Facebook'}
anuncios_google_presupuesto = {i for i, plataforma in asignaciones_presupuesto if plataforma == 'Google'}
anuncios_no_incluidos_presupuesto = set(range(n)) - anuncios_facebook_presupuesto - anuncios_google_presupuesto

# Maximización sin considerar presupuesto
def maximizar_sin_presupuesto(costos_facebook, impactos_facebook, costos_google, impactos_google, n):
    dp_sin_presupuesto = [[0, set()] for _ in range(2 ** n)]
    for i in range(2 ** n):
        impact_facebook = 0
        impact_google = 0
        current_set = set()
        for j in range(n):
            if i & (1 << j):
                impact_facebook += impactos_facebook[j]
                current_set.add((j, 'Facebook'))
            else:
                impact_google += impactos_google[j]
                current_set.add((j, 'Google'))
        dp_sin_presupuesto[i] = [impact_facebook + impact_google, current_set]
    return max(dp_sin_presupuesto, key=lambda x: x[0])

max_valor_ventas_sin_presupuesto, asignaciones_sin_presupuesto = maximizar_sin_presupuesto(costos_facebook, impactos_facebook, costos_google, impactos_google, n)

# Separar anuncios por plataforma sin presupuesto
anuncios_facebook_max = {i for i, plataforma in asignaciones_sin_presupuesto if plataforma == 'Facebook'}
anuncios_google_max = {i for i, plataforma in asignaciones_sin_presupuesto if plataforma == 'Google'}
anuncios_no_incluidos_max = set(range(n)) - anuncios_facebook_max - anuncios_google_max

# Imprimir resultados
print("Valor máximo de ventas con presupuesto:", valor_maximo_presupuesto)
print("Anuncios asignados a Facebook con presupuesto:", anuncios_facebook_presupuesto)
print("Anuncios asignados a Google con presupuesto:", anuncios_google_presupuesto)
print("Anuncios no incluidos en ninguna plataforma con presupuesto:", anuncios_no_incluidos_presupuesto)

print("Valor máximo de ventas sin presupuesto:", max_valor_ventas_sin_presupuesto)
print("Anuncios asignados a Facebook sin presupuesto:", anuncios_facebook_max)
print("Anuncios asignados a Google sin presupuesto:", anuncios_google_max)
print("Anuncios no incluidos en ninguna plataforma sin presupuesto:", anuncios_no_incluidos_max)
