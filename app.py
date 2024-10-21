from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/<name>")
def print_name(name):
    return f"Hello, {name}"


@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_age = request.form.get("age")
    return render_template("hello.html", name=input_name, age=input_age)


@app.route("/query", methods=["GET"])
def process_query_query():
    query = request.args.get("q")
    return process_query(query)


def process_query(string):
    if string == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"
    elif string == "asteroids":
        return "Unknown"
    else:
        return "Query not found"
