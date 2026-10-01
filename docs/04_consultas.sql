-- Q1 Máquinas em manutenção e mecânico da OS ativa
SELECT m.patrimonio, m.modelo, mc.nome AS mecanico, os.status FROM maquinas m JOIN ordens_servico os ON os.maquina_id=m.id JOIN mecanicos mc ON mc.id=os.mecanico_id WHERE os.status IN ('Aberta','Em andamento');
-- Q2 Custo por máquina, incluindo máquinas sem custo. A ordenação pode ser feita pela aplicação para RF10.
SELECT m.patrimonio, m.modelo, COALESCE(SUM(CASE WHEN os.status='Concluída' THEN COALESCE(os.horas_trabalhadas,0)*85 + COALESCE((SELECT SUM(i.quantidade*i.valor_unitario) FROM itens_os i WHERE i.os_id=os.id),0) ELSE 0 END),0) AS custo_total FROM maquinas m LEFT JOIN ordens_servico os ON os.maquina_id=m.id GROUP BY m.id;
-- Q3 Estoque abaixo do mínimo
SELECT * FROM pecas WHERE estoque < estoque_minimo;
-- Q4 Mecânicos e quantidade de OS concluídas em agosto/2026
SELECT mc.nome, COUNT(CASE WHEN os.status='Concluída' AND os.data_conclusao BETWEEN '2026-08-01' AND '2026-08-31' THEN 1 END) AS qtd FROM mecanicos mc LEFT JOIN ordens_servico os ON os.mecanico_id=mc.id GROUP BY mc.id;
-- Q5 OS abertas há mais de 7 dias em relação a 29/09/2026
SELECT * FROM ordens_servico WHERE status NOT IN ('Concluída','Cancelada') AND julianday('2026-09-29')-julianday(data_abertura)>7;
