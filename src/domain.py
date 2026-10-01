class Maquina:
    def __init__(self, id, patrimonio, tipo, modelo, ano, horimetro_atual, horimetro_ultima_preventiva, status):
        self.id=id; self.patrimonio=patrimonio; self.tipo=tipo; self.modelo=modelo; self.ano=ano
        self.horimetro_atual=horimetro_atual; self.horimetro_ultima_preventiva=horimetro_ultima_preventiva; self.status=status
    def precisa_preventiva(self): return (self.horimetro_atual-self.horimetro_ultima_preventiva)>=250
    def pode_receber_os(self): return self.status == 'Ativa'

class Mecanico:
    def __init__(self,id,nome,especialidade,ativo): self.id=id; self.nome=nome; self.especialidade=especialidade; self.ativo=bool(ativo)
    def pode_ser_atribuido(self): return self.ativo

class Peca:
    def __init__(self,id,codigo,nome,valor_unitario,estoque,estoque_minimo):
        self.id=id; self.codigo=codigo; self.nome=nome; self.valor_unitario=valor_unitario; self.estoque=estoque; self.estoque_minimo=estoque_minimo
    def estoque_baixo(self): return self.estoque < self.estoque_minimo

class ItemOS:
    def __init__(self,quantidade,valor_unitario): self.quantidade=quantidade; self.valor_unitario=valor_unitario
    def subtotal(self): return self.quantidade*self.valor_unitario

class OrdemServico:
    VALOR_HORA=85.0
    def __init__(self,tipo,descricao,horas=0,itens=None): self.tipo=tipo; self.descricao=descricao; self.horas=horas; self.itens=itens or []
    def calcular_custo_total(self): return self.horas*self.VALOR_HORA+sum(i.subtotal() for i in self.itens)
