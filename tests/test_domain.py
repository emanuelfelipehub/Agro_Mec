import sys, os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','src'))
from domain import Maquina, ItemOS, OrdemServico

def test_custo_total():
    os=OrdemServico('Preventiva','Revisão',5,[ItemOS(1,68.90),ItemOS(1,54.50),ItemOS(1,489.90)])
    assert round(os.calcular_custo_total(),2)==1038.30

def test_preventiva_limite():
    assert not Maquina(1,'PAT','Trator','X',2020,1549,1300,'Ativa').precisa_preventiva()
    assert Maquina(1,'PAT','Trator','X',2020,1550,1300,'Ativa').precisa_preventiva()
