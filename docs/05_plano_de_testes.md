# Plano de testes — AgroMec

| ID | Req/RN | Cenário | Esperado | Técnica | Nível |
|---|---|---|---|---|---|
| CT01 | RF01/RNF01 | Login gerente/Saep@2026 | Acesso ao painel | Caixa-preta | Sistema |
| CT02 | RF01/RNF01 | Senha incorreta | Acesso negado | Partição | Sistema |
| CT03 | RN01 | Abrir OS para máquina em manutenção | Bloqueio | Partição | Integração |
| CT04 | RN06 | Atribuir mecânico inativo | Bloqueio | Partição | Integração |
| CT05 | RN03 | Adicionar quantidade maior que estoque | Bloqueio | Valor-limite | Integração |
| CT06 | RN02 | Concluir com 0 horas | Bloqueio | Valor-limite | Integração |
| CT07 | RN02 | Data conclusão anterior à abertura | Bloqueio | Valor-limite | Integração |
| CT08 | RN05 | Diferença 249 h | Sem alerta | Valor-limite | Unidade |
| CT09 | RN05 | Diferença 250 h | Alerta | Valor-limite | Unidade |
| CT10 | RF10 | Relatório de custos | Decrescente por Insertion Sort | Caixa-preta | Sistema |
| CT11 | RF11/RNF01 | Busca com `' OR 1=1 --` | Não executa SQL malicioso | Segurança | Integração |
| CT12 | RN08 | Cancelar OS com peças | Estoque devolvido | Caixa-preta | Integração |

## Execução esperada
Os testes automatizados CT08/CT09 e cálculo de custo são executados em `tests/test_domain.py`. Os demais devem ser executados manualmente na interface e registrados com prints na entrega real.

## Defeitos simulados/corrigidos
- D01: tentativa de abrir OS em máquina em manutenção — corrigido com validação backend.
- D02: tentativa de concluir sem horas — corrigido com validação de valor > 0.
