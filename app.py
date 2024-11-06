from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import math

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Comentario_sql.db'
db = SQLAlchemy(app)

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    comentario = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Comentario {self.nome}>'

#começo da página
@app.route('/')
def index():
    comentarios = Comentario.query.all()
    return render_template('index.html', comentarios= comentarios)

#adicionar comentário
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        nome = request.form['nome']
        comentario = request.form['comentario']
        novo_Comentario = Comentario(nome=nome, comentario=comentario)
        db.session.add(novo_Comentario)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('comentario.html')

#adicionar comentário
@app.route('/curriculo', methods=['GET', 'POST'])
def currículo():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('curriculo.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
