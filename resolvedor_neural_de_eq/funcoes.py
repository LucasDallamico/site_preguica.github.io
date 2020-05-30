import numpy as np
from random import randint
import math
import sys

from pybrain3.tools.shortcuts import buildNetwork # para criar a rede
from pybrain3.datasets import SupervisedDataSet
from pybrain3.supervised.trainers import BackpropTrainer #algoritmo para treinar
import pickle #para salvar o treino
import csv
from pybrain3.structure import FeedForwardNetwork
from pybrain3.structure import LinearLayer, TanhLayer, SigmoidLayer, GaussianLayer
from pybrain3.structure import FullConnection

# -----------------------------------------------------------------
def cria_rede():
    """

    :rtype:
    """
    #                   Cria a rede neural
    network = FeedForwardNetwork()

    #                   DEFINIÇÕES DA REDE
    camadaEntrada = LinearLayer(1)      #1 neuronio de entrada
    camadaIntermediaria1 = TanhLayer(90) #4 neuronios na 1a camada intermediaria
    camadaIntermediaria2 = TanhLayer(90) #4 neuronios na 2a camada intermediaria
    camadaIntermediaria3 = TanhLayer(90)
    camadaIntermediaria4 = TanhLayer(90)
    camadaIntermediaria5 = TanhLayer(90)
    camadaIntermediaria6 = TanhLayer(90)
    camadaSaida = LinearLayer(1)        #1 neuronio de saida

    #                    CONFIGURA A REDE
    network.addInputModule(camadaEntrada)
    network.addModule(camadaIntermediaria1)
    network.addModule(camadaIntermediaria2)
    network.addModule(camadaIntermediaria3)
    network.addModule(camadaIntermediaria4)
    network.addModule(camadaIntermediaria5)
    network.addModule(camadaIntermediaria6)
    network.addOutputModule(camadaSaida)

    #                   CONECTA AS CAMADAS
    entrada_meio1 = FullConnection(camadaEntrada,camadaIntermediaria1)
    meio1_meio2 = FullConnection(camadaIntermediaria1,camadaIntermediaria2)
    meio2_meio3 = FullConnection(camadaIntermediaria2,camadaIntermediaria3)
    meio3_meio4 = FullConnection(camadaIntermediaria3,camadaIntermediaria4)
    meio4_meio5 = FullConnection(camadaIntermediaria4,camadaIntermediaria5)
    meio5_meio6 = FullConnection(camadaIntermediaria5,camadaIntermediaria6)
    meio4_saida = FullConnection(camadaIntermediaria6,camadaSaida)

    #                ADICIONA AS CAMADAS Á REDE
    network.addConnection(entrada_meio1)
    network.addConnection(meio1_meio2)
    network.addConnection(meio2_meio3)
    network.addConnection(meio3_meio4)
    network.addConnection(meio4_meio5)
    network.addConnection(meio5_meio6)
    network.addConnection(meio4_saida)

    network.sortModules() #Torna a rede utilizavel, faz as ligações

    ds = SupervisedDataSet(1,1) #1 entrada, 1 saida
    return network,ds

# -----------------------------------------------------------------
def treina_valor_rede(rede,ds,xo,y):
    ds.addSample(xo,y)
    #                      APRENDER
    trainer = BackpropTrainer(rede,ds,learningrate=0.02)
    trainer.train()
    return 1

# -----------------------------------------------------------------
"""
Gera o tipo de função aleatoriamente
1 -> Função de 1º grau
2 -> Função de 2º grau
3 -> Função de 3º grau
"""

def tipo_funcao():
      aleatorio = randint(1,3)
      return aleatorio
# -----------------------------------------------------------------

"""
Gera uma função aleatória de 1º grau no formato ax + b
"""
def gera_funcao_1():
	a = randint(-100,100)
	b = randint(-100,100)
	while(a == 0):
		a = randint(-100,100)
	while(b == 0):
		b = randint(-100,100)
	return(a,b)
# -----------------------------------------------------------------
"""
Gera uma função aleatória de 2º grau no formato ax² + b
"""
def gera_funcao_2():
	a = randint(-100,100)
	b = randint(-100,100)
	while(a == 0):
		a = randint(-100,100)
	while(b == 0):
		b = randint(-100,100)
	return(a,b)
# -----------------------------------------------------------------
"""
Gera uma função aleatória de 3º grau no formato ax³ + bx² + cx + d
"""
def gera_funcao_3():
	a = randint(-100,100)
	b = randint(-100,100)
	c = randint(-100,100)
	d = randint(-100,100)
	while(a == 0):
		a = randint(-100,100)
	while(b == 0):
		b = randint(-100,100)
	while(c == 0):
		a = randint(-100,100)
	while(d == 0):
		b = randint(-100,100)
	return(a,b,c,d)
# -----------------------------------------------------------------
"""
Resolve função de 1º e 3º grau
"""
def bisseccao(f,a,b,TOL=1e-4,NMAX=1000, output = False):
	#assert ( f(a)*f(b) < 0), " F(a) e F(b) devem ter valores diferentes"
	assert(b > a), "B deve ser maior que A"
	i = 0
	while (0.5*(b-a) > TOL) and (i < NMAX):
		i = i + 1
		p = (b+a) * 0.5
		if (output):
			print("Iteração ",i,": ",p)
		if f(p) == 0:
		  break
		if (f(a)*f(p) < 0):
			b = p
		else:
			a = p
	assert (i<NMAX), "Numero maximo de iterações foi atigindo"
	#return i,p,(0.5*(b-a))
	return p
# -----------------------------------------------------------------
def loge(n,li,ls):
    if math.fabs(li-ls) <= 0.000001:
       return (li+ls)/2.0
    if (math.exp(li)-n)*(math.exp((li+ls)/2.0)-n) < 0:
       return loge(n,li,(li+ls)/2.0)
    else:
       return loge(n,(li+ls)/2.0,ls)

def ln(n):
    if n == 0 or n < 0:
       return "Math Domain Error"
    if n == 1:
       return 0
    if n > 0 and n < 1:
       return loge(n,0,-n-80)
    else:
       return loge(n,0,n)