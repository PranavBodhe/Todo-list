from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
import pytz
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy(app)
ist = pytz.timezone('Asia/Kolkata')

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Pending")
    priority = db.Column(db.String(50), nullable=False, default="Medium")
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(ist))

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        status = request.form['status']
        priority = request.form['priority']
        project = Todo(title=title, desc=desc, status=status, priority=priority)
        db.session.add(project)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/search")
def search():
    query = request.args.get('query')
    results = Todo.query.filter(Todo.title.like(f"%{query}%")).all()
    return render_template("search_results.html", results=results, query=query)



@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        todo.status = request.form['status']
        if todo.status == "Completed":
            todo.priority = "Done"
        else:
            todo.priority = request.form['priority']

        db.session.commit()
        return redirect("/")
    return render_template('update.html', todo=todo)




@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=9000)
