from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    titulo = 'Hola!'
    lista = ['Luis', 'Paco', 'Pedro']
    return render_template("index.html", titulo=titulo, lista=lista)

@app.route("/hola")
def hola():
    return "<h3> Saludo desde Hola </h3>"

@app.route("/user/<string:user>")
def user(user):
    return "Hola " + user

@app.route("/numero/<int:n>")
def numero(n):
    return "Numero: {}".format(n)

@app.route("/user/<int:id>/<string:username>")
def username(id, username):
    return "ID {} nombre: {}".format(id, username)

@app.route("/suma/<int:n1>/<int:n2>")
def func(n1, n2):
    return "la suma es: {}".format(n1 + n2)

if __name__ == "__main__":
    app.run(debug=True)