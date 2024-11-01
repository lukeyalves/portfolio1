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

#calculadora
@app.route('/calculadora', methods=['GET', 'POST'])
def calcular():
    if request.method == 'POST':
        # Pegue os valores enviados pelo formulário
        operacao = request.form.get('operacao')
        num1 = float(request.form.get('num1'))
        
        # Para operações com dois números, verificar se o segundo número foi passado
        if operacao in ['soma', 'subtracao', 'multiplicacao', 'divisao', 'potencia']:
            num2 = float(request.form.get('num2'))

        resultado = ""
        
        try:
            if operacao == 'soma':
                resultado = num1 + num2
            elif operacao == 'subtracao':
                resultado = num1 - num2
            elif operacao == 'multiplicacao':
                resultado = num1 * num2
            elif operacao == 'divisao':
                if num2 != 0:
                    resultado = num1 / num2
                else:
                    resultado = "Erro: Divisão por zero"
            elif operacao == 'potencia':
                resultado = num1 ** num2
            elif operacao == 'raiz':
                if num1 >= 0:
                    resultado = math.sqrt(num1)
                else:
                    resultado = "Erro: Raiz quadrada de número negativo"
            elif operacao == 'seno':
                resultado = math.sin(math.radians(num1))
            elif operacao == 'cosseno':
                resultado = math.cos(math.radians(num1))
            elif operacao == 'tangente':
                resultado = math.tan(math.radians(num1))
        
        except ValueError:
            resultado = "Erro: Entrada inválida"
        
        # Renderize o template com o resultado
        return render_template('calculadora.html', resultado=resultado)

    # Se for uma requisição GET, apenas exiba o formulário da calculadora
    return render_template('calculadora.html', resultado=None)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
