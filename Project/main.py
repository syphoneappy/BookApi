from flask import *
import json,os
from flask_sqlalchemy import SQLAlchemy

from urllib.request import urlopen


app = Flask(__name__)
app.secret_key= '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////python/python/bookApi/BookApi/database.db'
db = SQLAlchemy(app)

api = "https://www.googleapis.com/books/v1/volumes?q=filter=free-ebooks:"
apiSession = "https://www.googleapis.com/books/v1/volumes?q=filter=ebooks:"
apiSearch = "https://www.googleapis.com/books/v1/volumes?q=intitle:"


class user(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120),  nullable=False, index=True, unique=True)
    password = db.Column(db.String(80))

class cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    title = db.Column(db.String(80))

db.create_all()


@app.route("/")
def front():
    resp = urlopen(api)
    book_data = json.load(resp)
    book =  book_data["items"]
    Maps = map(lambda datum: datum['volumeInfo'], book)
    return render_template('index.html',vol = Maps)

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        
        login = user.query.filter_by(email=uname, password=passw).first()
        if login is not None:
            session['loggedin'] = True
            session['user'] = uname
            return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/home")
def home():
    if session:
        resp = urlopen(apiSession)
        book_data = json.load(resp)
        book =  book_data["items"]
        Maps = map(lambda datum: datum['volumeInfo'], book)
        return render_template("index.html",vol = Maps)
    else:
        return render_template("404.html")

@app.route("/register",methods=["GET", "POST"])
def register():
    if request.method == "POST":
        mail = request.form['mail']
        passw = request.form['passw']
        register = user(email = mail, password = passw)
        db.session.add(register)
        db.session.commit()
        flash("Commited")
        return redirect(url_for("login"))
    return render_template("Credential.html")

@app.route("/inventory")
def newAdd():
    try:
        users = cart.query.filter_by(email=session['user']).all()
        resp = urlopen(apiSession)
        book_data = json.load(resp)
        book =  book_data["items"]
        Maps = map(lambda datum: datum['volumeInfo'], book)
        if session['user']:
            return render_template("cart.html",data = Maps,users=users)
        return render_template("cart.html",users = users)
    except:
        return render_template("404.html")


@app.route("/additem/<string:id_data>",methods=["POST"])
def add(id_data):
    product = cart(email = session['user'],title = id_data)
    db.session.add(product)
    db.session.commit()
    return redirect("/inventory")

@app.route("/remove/<int:id_data>",methods = ["POST"])
def remove(id_data):
    obj = cart.query.filter_by(id = id_data).one()
    db.session.delete(obj)
    db.session.commit()
    flash("Commited")
    return render_template("cart.html")

@app.route('/LogOut')
def LogOut():
    session.pop('loggedin',None)
    session.pop('user',None)
    session.clear()
    return redirect("/")

    




if __name__ == "__main__":
    app.run(debug=True)