from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
import random

g_usuario = "minerei@jix.im"
g_senha = "lucass2156"

class Gerador(Agent):
    a = random.randint(-100,100)
    b = random.randint(1,2)
    c = random.randint(1,3)
   
    class funcao(CyclicBehaviour):
        async def run(self):
            res = await self.receive(timeout=15)
            if res:
                x = float(res.body)
                x = float( Gerador.a + (Gerador.b/Gerador.c)**x )
                print("Enviou para " + str(res.sender) + " f(",res.body,")= ",x)
                msg = Message(to=str(res.sender)) 
                msg.set_metadata("performative", "subscribe")  
                msg.body = str(float(x)) # Alteracao
                await self.send(msg)
   
    async def setup(self):
        t = Template()
        t.set_metadata("performative","subscribe")

        tf = self.funcao()
        print("Funcao: ", Gerador.a, "+ (", Gerador.b / Gerador.c , ")^x")
        self.add_behaviour(tf,t)

gerador = Gerador(g_usuario, g_senha)
gerador.start()
