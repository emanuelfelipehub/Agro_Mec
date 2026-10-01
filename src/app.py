import os,sqlite3
from flask import Flask,render_template,request,redirect,url_for,session,flash,jsonify
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
from domain import Maquina,Mecanico,ItemOS
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); DB=os.path.join(BASE,'agromec.db')
app=Flask(__name__,template_folder='../templates',static_folder='../static'); app.secret_key=os.environ.get('AGROMEC_SECRET','agromec-chave-local-2026')
def db():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; c.execute('PRAGMA foreign_keys=ON'); return c
def q(sql,p=(),one=False):
 c=db()
 try:
  r=c.execute(sql,p); out=r.fetchone() if one else r.fetchall(); c.commit(); return out
 finally:c.close()
def init_db():
 c=db(); ddl=open(os.path.join(BASE,'docs','02_ddl.sql'),encoding='utf8').read().split('-- DCL')[0]; c.executescript(ddl)
 if c.execute('SELECT COUNT(*) FROM usuarios').fetchone()[0]==0:
  c.execute('INSERT INTO usuarios(nome,login,senha_hash) VALUES(?,?,?)',('Osvaldo Ribeiro','gerente',generate_password_hash('Saep@2026')))
  c.executemany('INSERT INTO maquinas(patrimonio,tipo,modelo,ano,horimetro_atual,horimetro_ultima_preventiva,status) VALUES(?,?,?,?,?,?,?)',[("PAT-001","Trator","John Deere 6110J",2019,1480,1300,"Ativa"),("PAT-002","Colheitadeira","Case IH 7150",2020,2240,1980,"Em manutenção"),("PAT-003","Pulverizador","Jacto Uniport 3030",2021,1120,900,"Ativa"),("PAT-004","Trator","Massey Ferguson 4707",2018,3350,3100,"Ativa"),("PAT-005","Plantadeira","Tatu Marchesan PST",2022,640,500,"Em manutenção"),("PAT-006","Trator","New Holland T7.245",2017,4119,3870,"Ativa")])
  c.executemany('INSERT INTO mecanicos(nome,especialidade,ativo) VALUES(?,?,?)',[('Anderson Teixeira','Motores diesel',1),('Bruna Rezende','Hidráulica',1),('Carlos Eduardo Lima','Elétrica',1),('Daniela Sousa','Transmissão',1),('Elias Moraes','Motores diesel',0)])
  c.executemany('INSERT INTO pecas(codigo,nome,valor_unitario,estoque,estoque_minimo) VALUES(?,?,?,?,?)',[('P001','Filtro de óleo do motor',68.90,25,10),('P002','Filtro de combustível',54.50,18,8),('P003','Filtro de ar primário',132,6,8),('P004','Óleo 15W40 (balde 20 L)',489.90,9,4),('P005','Correia do alternador',76.30,4,5),('P006','Mangueira hidráulica 3/4"',214,7,3),('P007','Bico de pulverização (un.)',38.70,40,20),('P008','Bateria 12V 150Ah',899,2,2)])
  data=[(1,'PAT-001','Anderson Teixeira','Preventiva','Revisão 250 h: óleo e filtros','2026-08-05','2026-08-06',5,'Concluída'),(2,'PAT-002','Bruna Rezende','Corretiva','Vazamento na linha hidráulica','2026-08-12','2026-08-14',7.5,'Concluída'),(3,'PAT-003','Carlos Eduardo Lima','Corretiva','Falha elétrica na barra','2026-08-18','2026-08-18',3,'Concluída'),(4,'PAT-004','Carlos Eduardo Lima','Corretiva','Troca da correia do alternador','2026-08-25','2026-08-26',3,'Concluída'),(5,'PAT-002','Daniela Sousa','Corretiva','Ruído na transmissão','2026-09-15',None,None,'Em andamento'),(6,'PAT-005','Bruna Rezende','Preventiva','Revisão geral pré-plantio','2026-09-25',None,None,'Aberta'),(7,'PAT-006','Carlos Eduardo Lima','Corretiva','Bateria descarregada','2026-09-02','2026-09-02',1.5,'Concluída'),(8,'PAT-001','Bruna Rezende','Corretiva','Mangueira hidráulica rompida','2026-09-10',None,None,'Cancelada')]
  for n,pat,mec,tipo,desc,ab,co,h,st in data:
   mid=c.execute('SELECT id FROM maquinas WHERE patrimonio=?',(pat,)).fetchone()[0]; mc=c.execute('SELECT id FROM mecanicos WHERE nome=?',(mec,)).fetchone()[0]
   c.execute('INSERT INTO ordens_servico(id,maquina_id,mecanico_id,tipo,descricao,data_abertura,data_conclusao,horas_trabalhadas,status) VALUES(?,?,?,?,?,?,?,?,?)',(n,mid,mc,tipo,desc,ab,co,h,st))
  for oid,code,qty,val in [(1,'P001',1,68.9),(1,'P002',1,54.5),(1,'P004',1,489.9),(2,'P006',2,214),(3,'P008',1,899),(4,'P005',1,76.3),(7,'P008',1,899)]:
   pid=c.execute('SELECT id FROM pecas WHERE codigo=?',(code,)).fetchone()[0]; c.execute('INSERT INTO itens_os(os_id,peca_id,quantidade,valor_unitario) VALUES(?,?,?,?)',(oid,pid,qty,val))
  c.commit()
 c.close()
def auth(f):
 @wraps(f)
 def w(*a,**k):
  if 'user_id' not in session:return redirect(url_for('login'))
  return f(*a,**k)
 return w
@app.route('/login',methods=['GET','POST'])
def login():
 if request.method=='POST':
  u=q('SELECT * FROM usuarios WHERE login=?',(request.form.get('login','').strip(),),True)
  if u and check_password_hash(u['senha_hash'],request.form.get('senha','')):session['user_id']=u['id'];session['nome']=u['nome'];return redirect(url_for('index'))
  flash('Usuário ou senha inválidos.','danger')
 return render_template('login.html')
@app.get('/logout')
def logout():session.clear();return redirect(url_for('login'))
@app.get('/')
@auth
def index():
 ms=q('SELECT * FROM maquinas'); alert=[m for m in ms if Maquina(**dict(m)).precisa_preventiva()]; low=q('SELECT * FROM pecas WHERE estoque<estoque_minimo'); active=q("SELECT os.*,m.patrimonio,mc.nome mecanico FROM ordens_servico os JOIN maquinas m ON m.id=os.maquina_id JOIN mecanicos mc ON mc.id=os.mecanico_id WHERE os.status IN ('Aberta','Em andamento')")
 return render_template('index.html',maquinas=ms,alertas=alert,baixo=low,abertas=active)
@app.route('/maquinas',methods=['GET','POST'])
@auth
def maquinas():
 if request.method=='POST':
  try:
   f=request.form;q('INSERT INTO maquinas(patrimonio,tipo,modelo,ano,horimetro_atual,horimetro_ultima_preventiva,status) VALUES(?,?,?,?,?,?,?)',(f['patrimonio'],f['tipo'],f['modelo'],int(f['ano']),float(f['horimetro_atual']),float(f['horimetro_ultima_preventiva']),f['status']));flash('Máquina cadastrada.','success')
  except sqlite3.IntegrityError:flash('Patrimônio já cadastrado.','danger')
  except:flash('Dados inválidos.','danger')
  return redirect(url_for('maquinas'))
 return render_template('maquinas.html',maquinas=q('SELECT * FROM maquinas'))
@app.post('/maquinas/<int:id>/excluir')
@auth
def excluir(id):
 if q('SELECT COUNT(*) n FROM ordens_servico WHERE maquina_id=?',(id,),True)['n']>0:flash('Exclusão bloqueada: há OS vinculadas.','danger')
 else:q('DELETE FROM maquinas WHERE id=?',(id,));flash('Máquina excluída.','success')
 return redirect(url_for('maquinas'))
@app.get('/mecanicos')
@auth
def mecanicos():return render_template('mecanicos.html',mecanicos=q('SELECT * FROM mecanicos'))
@app.post('/mecanicos/<int:id>/toggle')
@auth
def toggle(id):q('UPDATE mecanicos SET ativo=CASE ativo WHEN 1 THEN 0 ELSE 1 END WHERE id=?',(id,));return redirect(url_for('mecanicos'))
@app.route('/pecas',methods=['GET','POST'])
@auth
def pecas():
 if request.method=='POST':
  try:
   f=request.form;q('INSERT INTO pecas(codigo,nome,valor_unitario,estoque,estoque_minimo) VALUES(?,?,?,?,?)',(f['codigo'],f['nome'],float(f['valor_unitario']),int(f['estoque']),int(f['estoque_minimo'])));flash('Peça cadastrada.','success')
  except:flash('Não foi possível cadastrar a peça.','danger')
  return redirect(url_for('pecas'))
 return render_template('pecas.html',pecas=q('SELECT * FROM pecas'))
@app.route('/os',methods=['GET','POST'])
@auth
def ordens():
 if request.method=='POST':
  f=request.form;m=q('SELECT * FROM maquinas WHERE id=?',(int(f['maquina_id']),),True);mc=q('SELECT * FROM mecanicos WHERE id=?',(int(f['mecanico_id']),),True)
  if not m or not Maquina(**dict(m)).pode_receber_os():flash('A máquina está em manutenção.','danger')
  elif not mc or not Mecanico(**dict(mc)).pode_ser_atribuido():flash('Mecânico inativo.','danger')
  else:q("INSERT INTO ordens_servico(maquina_id,mecanico_id,tipo,descricao,data_abertura,status) VALUES(?,?,?,?,?,'Aberta')",(m['id'],mc['id'],f['tipo'],f['descricao'],f['data_abertura']));q("UPDATE maquinas SET status='Em manutenção' WHERE id=?",(m['id'],));flash('OS aberta.','success')
  return redirect(url_for('ordens'))
 sql="""SELECT os.*,m.patrimonio,mc.nome mecanico,COALESCE(os.horas_trabalhadas,0)*85+COALESCE((SELECT SUM(i.quantidade*i.valor_unitario) FROM itens_os i WHERE i.os_id=os.id),0) custo FROM ordens_servico os JOIN maquinas m ON m.id=os.maquina_id JOIN mecanicos mc ON mc.id=os.mecanico_id WHERE 1=1""";p=[]
 if request.args.get('status'):sql+=' AND os.status=?';p.append(request.args['status'])
 if request.args.get('maquina'):sql+=' AND os.maquina_id=?';p.append(request.args['maquina'])
 sql+=' ORDER BY os.id DESC'
 return render_template('os.html',ordens=q(sql,p),maquinas=q('SELECT * FROM maquinas'),mecanicos=q('SELECT * FROM mecanicos WHERE ativo=1'))
@app.get('/os/<int:id>')
@auth
def detalhe(id):
 osr=q('SELECT os.*,m.patrimonio,mc.nome mecanico FROM ordens_servico os JOIN maquinas m ON m.id=os.maquina_id JOIN mecanicos mc ON mc.id=os.mecanico_id WHERE os.id=?',(id,),True);it=q('SELECT i.*,p.codigo,p.nome FROM itens_os i JOIN pecas p ON p.id=i.peca_id WHERE i.os_id=?',(id,)); custo=(osr['horas_trabalhadas'] or 0)*85+sum(x['quantidade']*x['valor_unitario'] for x in it)
 return render_template('os_detalhe.html',os=osr,itens=it,pecas=q('SELECT * FROM pecas'),custo=custo)
@app.post('/os/<int:id>/item')
@auth
def item(id):
 qty=int(request.form['quantidade']);p=q('SELECT * FROM pecas WHERE id=?',(int(request.form['peca_id']),),True);o=q('SELECT * FROM ordens_servico WHERE id=?',(id,),True)
 if o['status'] in ('Concluída','Cancelada'):flash('OS não permite alteração.','danger')
 elif qty<=0 or qty>p['estoque']:flash('Quantidade superior ao estoque.','danger')
 else:q('INSERT INTO itens_os(os_id,peca_id,quantidade,valor_unitario) VALUES(?,?,?,?)',(id,p['id'],qty,p['valor_unitario']));q('UPDATE pecas SET estoque=estoque-? WHERE id=?',(qty,p['id']));flash('Peça adicionada.','success')
 return redirect(url_for('detalhe',id=id))
@app.post('/os/<int:id>/status')
@auth
def status(id):
 o=q('SELECT * FROM ordens_servico WHERE id=?',(id,),True);new=request.form['status']
 if o['status']=='Concluída':flash('OS concluída não pode ser alterada.','danger');return redirect(url_for('detalhe',id=id))
 if new=='Concluída':
  try:h=float(request.form['horas']);d=request.form['data_conclusao'];assert h>0 and d>=o['data_abertura']
  except:flash('Horas devem ser maiores que zero e a data não pode ser anterior à abertura.','danger');return redirect(url_for('detalhe',id=id))
  q('UPDATE ordens_servico SET status=?,horas_trabalhadas=?,data_conclusao=? WHERE id=?',(new,h,d,id));q("UPDATE maquinas SET status='Ativa',horimetro_ultima_preventiva=CASE WHEN ?='Preventiva' THEN horimetro_atual ELSE horimetro_ultima_preventiva END WHERE id=?",(o['tipo'],o['maquina_id']))
 elif new=='Cancelada':
  for x in q('SELECT p.id,i.quantidade FROM itens_os i JOIN pecas p ON p.id=i.peca_id WHERE i.os_id=?',(id,)):q('UPDATE pecas SET estoque=estoque+? WHERE id=?',(x['quantidade'],x['id']))
  q("UPDATE ordens_servico SET status='Cancelada' WHERE id=?",(id,));q("UPDATE maquinas SET status='Ativa' WHERE id=?",(o['maquina_id'],))
 elif new=='Em andamento':q("UPDATE ordens_servico SET status='Em andamento' WHERE id=?",(id,))
 flash('Status atualizado.','success');return redirect(url_for('detalhe',id=id))
def insertion_sort(a):
 a=a[:]
 for i in range(1,len(a)):
  key=a[i];j=i-1
  while j>=0 and a[j]['custo']<key['custo']:a[j+1]=a[j];j-=1
  a[j+1]=key
 return a
def busca_sequencial(a,pat):
 for x in a:
  if x['patrimonio'].lower()==pat.lower():return x
 return None
@app.get('/relatorio')
@auth
def relatorio():
 rows=q("SELECT os.*,m.patrimonio,m.modelo,mc.nome mecanico,COALESCE(os.horas_trabalhadas,0)*85+COALESCE((SELECT SUM(i.quantidade*i.valor_unitario) FROM itens_os i WHERE i.os_id=os.id),0) custo FROM ordens_servico os JOIN maquinas m ON m.id=os.maquina_id JOIN mecanicos mc ON mc.id=os.mecanico_id WHERE os.status='Concluída'");return render_template('relatorio.html',ordens=insertion_sort([dict(x) for x in rows]))
@app.get('/busca')
@auth
def busca():
 t=request.args.get('patrimonio','');return render_template('busca.html',termo=t,maquina=busca_sequencial(q('SELECT * FROM maquinas'),t) if t else None)
@app.post('/api/horimetro')
def sensor():
 d=request.get_json(silent=True) or {};pat=d.get('patrimonio');h=d.get('horimetro');m=q('SELECT * FROM maquinas WHERE patrimonio=?',(pat,),True)
 if not m:return jsonify(error='Patrimônio não encontrado'),404
 try:h=float(h)
 except:return jsonify(error='Horímetro inválido'),400
 if h<m['horimetro_atual']:return jsonify(error='Horímetro deve ser maior ou igual ao atual'),400
 q('UPDATE maquinas SET horimetro_atual=? WHERE id=?',(h,m['id']));mm=q('SELECT * FROM maquinas WHERE id=?',(m['id'],),True);return jsonify(ok=True,patrimonio=pat,horimetro=h,precisa_preventiva=Maquina(**dict(mm)).precisa_preventiva())
init_db()
if __name__=='__main__':app.run(debug=True)
