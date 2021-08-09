from flask import Flask, render_template, url_for, request, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eyes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/member')
def member():
    members = Article.query.order_by(Article.date).all()
    return render_template("member.html", members=members)

@app.route('/member/<int:id>')
def member_about(id):
    member = Article.query.get(id)
    return render_template("member_about.html", member=member)


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']

        article = Article(title=title, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/member')
        except:
            return "ERROR WHILE ADDING A NEW MEMBER"
    else:
        return render_template("create-article.html")



if __name__ == "__main__":
    app.run(debug=True)
