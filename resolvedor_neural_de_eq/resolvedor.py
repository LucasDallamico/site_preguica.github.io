# -*- coding: utf-8 -*-
# ____________________________________________________________________
#                       BIBLIOTECAS
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template
from spade import quit_spade
import os
import random
import sys
import math
import time
import asyncio
import funcoes as f

# ____________________________________________________________________
#           Acessos ao servidor jix.im
r_usuario = "dallamico@jix.im"
r_senha = "Beleminerei19"
# g_usuario = "aulaufsc@jix.im"
g_usuario = "minerei@jix.im"
# g_senha = "lucass2156"

# ____________________________________________________________________
#                       RESOLVEDOR
var_entr = f.np.zeros(1)  # para criar um array

class Resolvedor(Agent):
    class inicia_rede(OneShotBehaviour):
        async def run(self):
            Resolvedor.rede_neural, Resolvedor.data_set = f.cria_rede()
            Resolvedor.i = 0
            Resolvedor.j = 0
            Resolvedor.saidaRede = 0
            Resolvedor.a_professor = 0
            Resolvedor.bc_professor = 0

    class determina_eq_prof(OneShotBehaviour):
        async def  run(self):
            #Determina a
            msg = Message(to=g_usuario)
            msg.set_metadata("performative", "subscribe")
            msg.body = str(0)
            await self.send(msg)
            msg = await self.receive(timeout=15)
            Resolvedor.a_professor = float(msg.body) - 1
            #Determinando (B/C)**x
            msg = Message(to=g_usuario)
            msg.set_metadata("performative", "subscribe")
            msg.body = str(1)
            await self.send(msg)
            msg = await self.receive(timeout=15)
            Resolvedor.bc_professor = float(msg.body) - Resolvedor.a_professor
            if ( Resolvedor.bc_professor == 0):
                Resolvedor.bc_professor = 1
            #print("--> A = ",Resolvedor.a_professor, ", BC = ", Resolvedor.bc_professor)

    class rede_treino(CyclicBehaviour):
        async def run(self):
            if ( Resolvedor.a_professor != 0):
                # Aprendizagem auxiliada
                if (Resolvedor.i <= 15):
                    msg = Message(to=g_usuario)
                    msg.set_metadata("performative", "subscribe")
                    msg.body = str(Resolvedor.j)
                    await self.send(msg)
                    msg = await self.receive(timeout=5)
                    if (msg):
                        var_entr[0] = float(msg.body)
                        z = Resolvedor.rede_neural.activate(var_entr)
                        Resolvedor.saidaRede = z
                        exato_valor_y = Resolvedor.a_professor + Resolvedor.bc_professor ** Resolvedor.j
                        f.treina_valor_rede(Resolvedor.rede_neural, Resolvedor.data_set, float(Resolvedor.saidaRede), exato_valor_y)
                        # ------ Mostra dados -------
                        print("-----------------------------")
                        print("Iteracao (x) = ",Resolvedor.i)
                        print("Y(Recebido)  = ", var_entr)
                        print("F(x)         = ",exato_valor_y)
                        print("Z(Rede)     = ",z)
                        print("-----------------------------")
                        # ---------------------------
                        if ( Resolvedor.i < 20):
                            Resolvedor.j += 1
                            Resolvedor.i += 1
                        if (  Resolvedor.i == 20):
                            Resolvedor.j = 0
                            Resolvedor.i += 1
                            print("Agora, testando o conhecimento da rede ... \n \n")
                else:
                    # Testa seu conhecimento
                    msg = Message(to=g_usuario)
                    msg.set_metadata("performative", "subscribe")
                    msg.body = str(Resolvedor.j)
                    await self.send(msg)
                    msg = await self.receive(timeout=5)
                    if (msg):
                        var_entr[0] = float(msg.body)
                        z = Resolvedor.rede_neural.activate(var_entr)
                        f.treina_valor_rede(Resolvedor.rede_neural, Resolvedor.data_set, float(Resolvedor.saidaRede),z)
                        Resolvedor.saidaRede = z
                        # ------ Mostra dados -------
                        print("-----------------------------")
                        print("Iteracao (x) = ", Resolvedor.i)
                        print("Y(Recebido)  = ", var_entr)
                        print("Z(Rede solo) = ", z)
                        print("-----------------------------")
                        # ---------------------------
                        if (Resolvedor.i == 40):
                            print("\n \n Finalizando o agente ...")
                            await self.agent.stop()
                        else:
                            Resolvedor.j += 1
                            Resolvedor.i += 1


    # --------------------------------
    async def setup(self):
        print("Resovedor iniciado !")
        self.rede_neural = None
        self.data_set = None
        self.i = None
        self.saidaRede = None
        self.a_professor = None
        self.bc_professor = None
        self.j = None

        temp = Template()
        temp.set_metadata("performative", "inform")
        b = self.inicia_rede()
        self.add_behaviour(b, temp)

        temp = Template()
        temp.set_metadata("performative", "subscribe")

        b = self.determina_eq_prof()
        self.add_behaviour(b,temp)

        temp = Template()
        temp.set_metadata("performative", "subscribe")
        c = self.rede_treino()
        self.add_behaviour(c, temp)
# -------------------------- MAIN  ----------------------------------
if __name__ == "__main__":
    os.system("clear")
    print("-------------------------------------------------")
    print("            RESOLVEDOR REDE NEURAL               ")
    print("-------------------------------------------------")
    print("-> Iniciando a comunicação do agente ...")
    print("Aguardar 5s para o garantir que o gerador esteja vivo ...")
    time.sleep(5)
    # Conecta o agente com o servidor
    a_resolvedor = Resolvedor(r_usuario, r_senha)
    ponto1 = a_resolvedor.start()
    ponto1.result()

    while (a_resolvedor.is_alive()):
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            a_resolvedor.stop()
            break
# ____________________________________________________________________
