from flask import Flask , render_template , redirect , url_for , request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message


app = Flask ( __name__ )
app.config [ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///testedb.db'
db = SQLAlchemy ( app )

mail= Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'folhaflaskapp@gmail.com'
app.config['MAIL_PASSWORD'] = 'batata21'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.before_first_request
def create_table() :
    db.create_all ()

class Todo ( db.Model ) :
    id = db.Column ( db.Integer , primary_key=True )
    content = db.Column ( db.String ( 200 ) , nullable=False )
    completed = db.Column ( db.Integer , default=0 )
    email = db.Column (db.String (200), nullable=False)
    date_created = db.Column ( db.DateTime , default=datetime.utcnow )

    def __repr__(self) :
        return '<Task %r>' % self.id


@app.route ( '/' , methods=[ 'POST' , 'GET' ] )
def index() :

    if request.method == 'POST' :
        task_content = request.form [ 'content' ]
        task_email = request.form [ 'email' ]
        new_task = Todo ( content=task_content, email=task_email )

        try :
            db.session.add ( new_task )
            db.session.commit ()
            return redirect ( '/' )
        except :
            return 'Problema ao add tarefa'

    else :

        dados = Todo.query.order_by ( Todo.date_created ).all ()

        return render_template ('index.html', dados = dados)


@app.route ( '/delete/<int:id>' )
def delete(id) :
    task_to_delete = Todo.query.get_or_404 ( id )

    try :
        db.session.delete ( task_to_delete )
        db.session.commit ()
        return redirect ( '/' )

    except :
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Erro ao atualizar'
    else:
        return render_template('update.html', task = task )


@app.route("/sendmail/<int:id>")
def sendmail(id):
        task_to_send = Todo.query.filter_by ( id = id ).first ()
        recipients = task_to_send.email
        body = task_to_send.content
        msg = Message(subject="Projeto de organização de tarefas",
                      sender='folhaflaskapp@gmail.com',
                      recipients=[recipients], # replace with your email for testing
                      body=body)
        mail.send(msg)
        return render_template('sendmail.html')




if __name__ == "__main__" :
    app.run ( debug=True )
