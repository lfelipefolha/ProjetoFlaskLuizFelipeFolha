from flask import Flask , render_template , redirect , url_for , request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message
import random
app = Flask ( __name__ ) #inicia uma aplicação utilizando Flask
app.config [ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///testedb.db' #configura a base de dados
db = SQLAlchemy ( app )

#nessa etapa é feita a configuração para enviar emails através da aplicação
mail= Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'folhaflaskapp@gmail.com' #email utilizado para o propósito
app.config['MAIL_PASSWORD'] = 'batata21'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


#cria a base de dados da aplicação
@app.before_first_request
def create_table() :
    db.create_all ()

#aqui é feita a modelagem do banco de dados
class Todo ( db.Model ) :
    id = db.Column ( db.Integer , primary_key=True )
    content = db.Column ( db.String ( 200 ) , nullable=False )
    completed = db.Column ( db.Integer , default=0 )
    email = db.Column (db.String (200), nullable=False)
    date_created = db.Column ( db.DateTime , default=datetime.utcnow )
    prazo = db.Column( db.String, nullable=False )

    def __repr__(self) :
        return '<Task %r>' % self.id


#define a rota inicial e cria a função principal da app
@app.route ( '/' , methods=[ 'POST' , 'GET' ] )
def index() :
    #faz a requisão dos dados do formulário
    if request.method == 'POST' :
        task_content = request.form [ 'content' ]
        task_email = request.form [ 'email' ]
        prazo = request.form [ 'prazo' ]
        new_task = Todo ( content=task_content, email=task_email, prazo = prazo )

        #add os dados no banco de dados
        try :
            db.session.add ( new_task )
            db.session.commit ()
            return redirect ( '/' )
        except :
            return 'Problema ao add tarefa'
    #devolve os dados já obtidos na tela principal
    else :

        dados = Todo.query.order_by ( Todo.date_created ).all ()

        return render_template ('index.html', dados = dados)

#função para deletar os dados que foram add
@app.route ( '/delete/<int:id>' )
def delete(id) :
    #solicita através do id de cada dado, caso não exista é retornado um código de erro
    task_to_delete = Todo.query.get_or_404 ( id )

    #apaga os dados obtidos
    try :
        db.session.delete ( task_to_delete )
        db.session.commit ()
        return redirect ( '/' )

    #retorna uma exceção caso ocorra algum erro
    except :
        return 'There was a problem deleting that task'

#funcao responsável por atualizar os dados
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        task.email = request.form [ 'email' ]
        task.prazo = request.form [ 'prazo' ]

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Erro ao atualizar'
    else:
        return render_template('update.html', task = task )

#função utilizada para enviar os emails
@app.route("/sendmail/<int:id>")
def sendmail(id):
        lista =["Se não houver vento, reme.",
            "Não limite seus desafios. Desafie seus limites.",
            "Minha missão na vida não é apenas sobreviver, mas prosperar.",
            "O que você procura está procurando você.",
            "Uma meta é um sonho com um prazo.",
            "Tente mover o mundo - o primeiro passo será mover a si mesmo.",
            "Disciplina é a ponte entre metas e realizações.",
            "Sorte é o que acontece quando a preparação encontra a oportunidade.",
            "Eu faço da dificuldade a minha motivação. A volta por cima vem na continuação."]
        frase = random.choice(lista)
        #através da id são obtidos os dados de tarefa e endereço de email
        task_to_send = Todo.query.filter_by ( id = id ).first ()
        recipients = task_to_send.email #destinatário
        body = (str(task_to_send.content) + "\nFrase do dia: " +  str(frase))  #tarefa

        #aqui é realizada a definição do email a ser enviado
        msg = Message(subject="Projeto de organização de tarefas",
                      sender='folhaflaskapp@gmail.com',
                      recipients=[recipients], # replace with your email for testing
                      body= str(body))

        mail.send(msg) #função que envia o email

        return render_template('sendmail.html')



if __name__ == "__main__" :
    app.run ( debug=True )
