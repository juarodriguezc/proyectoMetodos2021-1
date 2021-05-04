from proyecto_flask import app
from flask import render_template

@app.route('/')
def homepage():
    return render_template("homepage.html", title="Inicio")
@app.route('/solecuaciones/bolzano')
def bolzano():
    return render_template("bolzano.html", title="Método de Bolzano")
