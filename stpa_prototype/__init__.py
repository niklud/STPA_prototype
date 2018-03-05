from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, flash, url_for, redirect, render_template, abort
from stpa_prototype.fundamentals.goals import goals_blueprint

app = Flask(__name__)

app.config.from_pyfile('../config.py')
app.register_blueprint(goals_blueprint)
db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'system_goals'
    id = db.Column('todo_id', db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    text = db.Column(db.String)
    vcs_check = db.Column(db.Boolean)
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.vcs_check = False
        self.pub_date = datetime.utcnow()


@app.route('/')
def index():
    return render_template('index.html',
                           todos=Todo.query.order_by(Todo.id.asc()).all()
                           )


@app.route('/hello')
def hello_world():
    return 'Hello!!!! Werld!'


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        todo = Todo(request.form['title'], request.form['text'])
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new.html')


@app.route('/goals/<int:todo_id>', methods=['GET', 'POST'])
def show_or_update(todo_id):
    todo_item = Todo.query.get(todo_id)
    if request.method == 'GET':
        return render_template('view.html', todo=todo_item)
    todo_item.title = request.form['title']
    todo_item.text = request.form['text']
    todo_item.vcs_check = ('vcs_check.%d' % todo_id) in request.form
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
