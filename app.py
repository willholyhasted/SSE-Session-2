import re
import math

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
    elif "plus" in string:
        numbers = re.findall(r"\d+", string)
        numbers = [int(num) for num in numbers]
        result = str(sum(numbers))
        return result
    elif "Which of the following numbers is the largest:" in string:
        numbers = re.findall(r"\d+", string)
        numbers = [int(num) for num in numbers]
        biggest = str(max(numbers))
        return biggest
    elif "multiplied" in string:
        numbers = re.findall(r"\d+", string)
        numbers = [int(num) for num in numbers]
        value = 1
        for num in numbers:
            value = value * num
        value = str(value)
        return value
    elif ("Which of the following numbers is"
          " both a square and a cube:") in string:
        numbers = re.findall(r"\d+", string)
        numbers = [int(num) for num in numbers]
        correct = []
        for num in numbers:
            if math.sqrt(num) % 1 == 0 and math.cbrt(num) % 1 == 0:
                correct.append(num)
        return ' '.join(str(e) for e in correct)

    else:
        return "Query not found"
