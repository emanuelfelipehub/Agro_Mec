# AgroMec — Modelagem

## Casos de uso
**Ator:** Gerente.

- RF01 Autenticar login
- RF02 Gerenciar máquinas
- RF03 Gerenciar mecânicos
- RF04 Gerenciar peças/estoque
- RF05 Abrir OS
- RF06 Adicionar itens à OS
- RF07 Alterar andamento/concluir/cancelar OS
- RF08 Consultar OS
- RF09 Visualizar alertas de preventiva
- RF10 Emitir relatório de custos
- RF11 Buscar máquina por patrimônio

Relação: **Abrir OS** «include» **Validar máquina e mecânico**. **Concluir OS** «include» **Calcular custo total**.

## Diagrama de classes (Mermaid)
```mermaid
classDiagram
class Maquina { -id:int; -patrimonio:string; -horimetroAtual:float; -horimetroUltimaPreventiva:float; -status:string; +precisaPreventiva(); +podeReceberOS() }
class Mecanico { -id:int; -nome:string; -ativo:bool; +podeSerAtribuido() }
class Peca { -id:int; -codigo:string; -valorUnitario:float; -estoque:int; +estoqueBaixo() }
class OrdemServico { -id:int; -tipo:string; -status:string; -horas:float; +calcularCustoTotal() }
class ItemOS { -quantidade:int; -valorUnitario:float; +subtotal() }
Maquina "1" --> "0..*" OrdemServico
Mecanico "1" --> "0..*" OrdemServico
OrdemServico "1" --> "1..*" ItemOS
Peca "1" --> "0..*" ItemOS
```
