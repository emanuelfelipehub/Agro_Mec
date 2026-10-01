-- Carga lógica do Anexo A. A aplicação também realiza esta carga automaticamente na primeira execução.
INSERT INTO usuarios(nome,login,senha_hash) VALUES ('Osvaldo Ribeiro','gerente','<HASH_GERADO_PELA_APLICACAO>');
INSERT INTO maquinas(patrimonio,tipo,modelo,ano,horimetro_atual,horimetro_ultima_preventiva,status) VALUES
('PAT-001','Trator','John Deere 6110J',2019,1480,1300,'Ativa'),('PAT-002','Colheitadeira','Case IH 7150',2020,2240,1980,'Em manutenção'),('PAT-003','Pulverizador','Jacto Uniport 3030',2021,1120,900,'Ativa'),('PAT-004','Trator','Massey Ferguson 4707',2018,3350,3100,'Ativa'),('PAT-005','Plantadeira','Tatu Marchesan PST',2022,640,500,'Em manutenção'),('PAT-006','Trator','New Holland T7.245',2017,4119,3870,'Ativa');
INSERT INTO mecanicos(nome,especialidade,ativo) VALUES ('Anderson Teixeira','Motores diesel',1),('Bruna Rezende','Hidráulica',1),('Carlos Eduardo Lima','Elétrica',1),('Daniela Sousa','Transmissão',1),('Elias Moraes','Motores diesel',0);
INSERT INTO pecas(codigo,nome,valor_unitario,estoque,estoque_minimo) VALUES ('P001','Filtro de óleo do motor',68.90,25,10),('P002','Filtro de combustível',54.50,18,8),('P003','Filtro de ar primário',132.00,6,8),('P004','Óleo 15W40 (balde 20 L)',489.90,9,4),('P005','Correia do alternador',76.30,4,5),('P006','Mangueira hidráulica 3/4"',214.00,7,3),('P007','Bico de pulverização (un.)',38.70,40,20),('P008','Bateria 12V 150Ah',899.00,2,2);
INSERT INTO ordens_servico(id,maquina_id,mecanico_id,tipo,descricao,data_abertura,data_conclusao,horas_trabalhadas,status) VALUES
(1,1,1,'Preventiva','Revisão 250 h: óleo e filtros','2026-08-05','2026-08-06',5,'Concluída'),
(2,2,2,'Corretiva','Vazamento na linha hidráulica','2026-08-12','2026-08-14',7.5,'Concluída'),
(3,3,3,'Corretiva','Falha elétrica na barra','2026-08-18','2026-08-18',3,'Concluída'),
(4,4,3,'Corretiva','Troca da correia do alternador','2026-08-25','2026-08-26',3,'Concluída'),
(5,2,4,'Corretiva','Ruído na transmissão','2026-09-15',NULL,NULL,'Em andamento'),
(6,5,2,'Preventiva','Revisão geral pré-plantio','2026-09-25',NULL,NULL,'Aberta'),
(7,6,3,'Corretiva','Bateria descarregada','2026-09-02','2026-09-02',1.5,'Concluída'),
(8,1,2,'Corretiva','Mangueira hidráulica rompida','2026-09-10',NULL,NULL,'Cancelada');
INSERT INTO itens_os(os_id,peca_id,quantidade,valor_unitario) VALUES (1,1,1,68.90),(1,2,1,54.50),(1,4,1,489.90),(2,6,2,214.00),(3,8,1,899.00),(4,5,1,76.30),(7,8,1,899.00);
