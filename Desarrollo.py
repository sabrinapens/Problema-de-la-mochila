'''Pseudocodigo recursivo del primer problema de la mochila visto
Si PesoMax <=0

Return

Si len(Pesos)==0

Si Suma(ValoresSelec)>MejorValor

MejorValor=Suma(ValoresSelec)

print(Mejor valor encontrado: MejorValor)

Return

Recursión que no incluye el elemento

Mochila =(Pesos[1:], Valores[1:], PesoMax, VSelec[:], PesosSelec[:])

Recursión que incluye el elemento

ValoresSelec.append(Valores[0])

PesosSelec.append(Pesos[0])

Mochila =(Pesos[1:], Valores[1:], PesoMax- Pesos[0], VSelec[:],
'''
#Prueba numero 2