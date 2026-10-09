from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Condominio, Usuario, Chamado

app = Flask(__name__)
app.secret_key = 'saas_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    if not Condominio.query.first():
        condo = Condominio(nome='Condomínio Central', endereco='Av. Principal, 100')
        db.session.add(condo)
        db.session.commit()
        
        morador = Usuario(condominio_id=condo.id, unidade='101', pin='1234', perfil='MORADOR')
        sindico = Usuario(condominio_id=condo.id, unidade='ADMIN', pin='9999', perfil='SINDICO')
        db.session.add_all([morador, sindico])
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        unidade = request.form.get('unidade')
        pin = request.form.get('pin')
        user = Usuario.query.filter_by(unidade=unidade, pin=pin).first()
        
        if user:
            session['user_id'] = user.id
            session['unidade'] = user.unidade
            session['perfil'] = user.perfil
            session['condominio_id'] = user.condominio_id
            
            if user.perfil == 'SINDICO':
                return redirect(url_for('dashboard'))
            return redirect(url_for('chamados'))
            
        flash('Unidade ou PIN inválidos!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/chamados', methods=['GET', 'POST'])
def chamados():
    if 'user_id' not in session or session.get('perfil') != 'MORADOR':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        novo_chamado = Chamado(
            condominio_id=session['condominio_id'],
            usuario_id=session['user_id'],
            titulo=titulo,
            descricao=descricao
        )
        db.session.add(novo_chamado)
        db.session.commit()
        return redirect(url_for('chamados'))

    lista = Chamado.query.filter_by(usuario_id=session['user_id']).order_by(Chamado.data_criacao.desc()).all()
    return render_template('morador.html', chamados=lista)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('perfil') != 'SINDICO':
        return redirect(url_for('login'))
    
    lista = Chamado.query.filter_by(condominio_id=session['condominio_id']).order_by(Chamado.data_criacao.desc()).all()
    return render_template('sindico.html', chamados=lista)

@app.route('/chamado/<int:id>/status', methods=['POST'])
def alterar_status(id):
    if 'user_id' not in session or session.get('perfil') != 'SINDICO':
        return redirect(url_for('login'))
    
    chamado = Chamado.query.get_or_404(id)
    novo_status = request.form.get('status')
    if novo_status:
        chamado.status = novo_status
        db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)