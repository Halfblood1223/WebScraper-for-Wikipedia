from flask import Flask, render_template, url_for, redirect, request, send_from_directory, abort, session
app = Flask(__name__)
app.secret_key = "hola"

@app.route('/')
def home():
    return render_template("homepage.html")

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        session["user"] = user
        return redirect(url_for("user"))
    else:
        return render_template('login.html')

@app.route('/user')
def user():
    if "user" in session:
        name = session["user"]
        return render_template('client.html', name = name)
    else:
        return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(port=8080,debug=True)
