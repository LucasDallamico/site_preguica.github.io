# -*- coding: utf-8 -*-
#____________________________________________________________________
    #                       BIBLIOTECAS
import time
import asyncio
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
from spade import quit_spade
import funcoes as f
import os

#____________________________________________________________________
#                      SERVIDOR JIX
# Registros do jix.im
#r_usuario = "dallamico@jix.im"
#r_senha = "Beleminerei19"
g_usuario = "minerei@jix.im"
g_senha = "lucass2156"

#____________________________________________________________________
#                       GERADOR
class Gerador(Agent):
    class escolhe_eq(OneShotBehaviour):
        async def run(self):
            #Gerador.grau_eq = f.tipo_funcao()
            Gerador.grau_eq = 1
            if(Gerador.grau_eq == 1):
                Gerador.m_a,Gerador.m_b = f.gera_funcao_1()
                print(Gerador.m_a,"x +",Gerador.m_b)
            elif(Gerador.grau_eq == 2):
                Gerador.m_a,Gerador.m_b = f.gera_funcao_2()
                print("x^2 + ",Gerador.m_a,"x +",Gerador.m_b)

            elif(Gerador.grau_eq == 3):
                Gerador.m_a,Gerador.m_b, Gerador.m_c, Gerador.m_d = f.gera_funcao_3()
                print(Gerador.m_a,"x³ + ",Gerador.m_b," x² + ", Gerador.m_c, " x + ", Gerador.m_d)
    # --------------------------------------

    class verifica(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                self.soma = 666
                int_x = 0.0
                #msg.body no formato '[1.3231]'
                aux_msg = msg.body.replace('[','')
                nova_msg = aux_msg.replace(']','')
                int_x = float(nova_msg)
                print("x = ",int_x)

                if(Gerador.grau_eq == 1):
                    self.soma = Gerador.m_a*int_x + Gerador.m_b

                if(Gerador.grau_eq == 2):
                    self.soma = int_x**2 + Gerador.m_a*(int_x) +  Gerador.m_b

                if(Gerador.grau_eq == 3):
                    self.soma =  Gerador.m_a*(int_x**3) + Gerador.m_b*(int_x**2) + Gerador.m_c*int_x + Gerador.m_d

                msg_s = Message(to=str(msg.sender))
                msg_s.set_metadata("performative","subscribe")
                # PQ O VALOR TEM QUE SER ENTRE 0 < X < 1
                if(abs(self.soma) < 1):
                    msg_s.body = "0"
                    self.soma = 0
                else:
                    msg_s.body = str(self.soma)

                await self.send(msg_s)
                print("Enviou para " + str(msg.sender) + " f(",msg.body,")= ",self.soma)


# -------- "INICIO DA CLASSE ---------------------"
    async def setup(self):
        print("Gerador inicializado!")
        self.grau_eq = 0
        self.m_a = 0
        self.m_b = 0

        self.t = Template()
        self.t.set_metadata("performative","inform")
        self.b = self.escolhe_eq()
        self.add_behaviour(self.b,self.t)

        #Verifica a resposta dos agentes
        self.behav3 = self.verifica()
        template3 = Template()
        template3.set_metadata("performative", "subscribe")
        self.add_behaviour(self.behav3,template3)

# -------------------------------------------------------------------
if __name__ == "__main__":
    os.system("clear")
    print("-------------------------------------------------")
    print("            GERADOR para rede neural             ")
    print("-------------------------------------------------")
    print("-> Iniciando a comunicação do agente ...")
    # Conecta o agente com o servidor
    a_gerador = Gerador(g_usuario,g_senha)
    ponto1 = a_gerador.start()
    ponto1.result() # aguardar até o agente ficar pronto

    while(a_gerador.is_alive()):
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            a_gerador.stop()
            break
