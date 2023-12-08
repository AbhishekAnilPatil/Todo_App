from flask import Flask, render_template, redirect, url_for, request
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
with app.app_context():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/flasktodo'
    db = SQLAlchemy(app)


    class Todo(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        text = db.Column(db.String(200))
        complete = db.Column(db.Boolean)

        def __str__(self):
            return f'{self.text}'

    db.create_all()
    obj = Todo()
    print(obj)
@app.route('/')
def index():
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()
    return render_template('index.html', incomplete=incomplete, complete=complete)

@app.route('/add', methods=['POST', 'GET'])
def add():
    todo = Todo(text=request.form['todoitem'], complete=False)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:id>')
def complete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    print(todo)
    todo.complete = True
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    obj = Todo.query.get(id)
    db.session.delete(obj)
    db.session.commit()
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)
