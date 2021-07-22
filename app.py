from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
import os
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://ejpqmwcnhklewj:252c88f39e2a84aacef2e6d6d5bbbd74c08e40f5a8922c091f8bc56579c613eb@ec2-35-171-57-132.compute-1.amazonaws.com:5432/d7lo78m49po7m1"
db = SQLAlchemy(app)


class Tasky(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"{self.sno} - {self.title}"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        task = Tasky(title=title,
                        description=description)
        db.session.add(task)
        db.session.commit()
    tasks = Tasky.query.all()
    return render_template("index.html", tasks=tasks)

@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        task = Tasky.query.filter_by(sno=sno).first()
        task.title = title
        task.description = description
        db.session.add(task)
        db.session.commit()
        return redirect('/')
    task = Tasky.query.filter_by(sno=sno).first()
    return render_template("update.html", task=task)


@app.route("/delete/<int:sno>")
def delete(sno):
    tasks = Tasky.query.filter_by(sno=sno).first()
    db.session.delete(tasks)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
