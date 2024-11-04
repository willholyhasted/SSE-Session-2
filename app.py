import re
import requests

from flask import Flask, render_template, request

app = Flask(__name__)


def make_request(username):
    response = requests.get(f"https://api.github.com/users/{username}/repos")
    repos_list = []
    repos_dates = []
    last_commits = []
    pushes_count = []  # To hold the number of pushes (commits) for each repo

    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            repos_list.append(repo["full_name"])
            repos_dates.append(repo["updated_at"])

            # Get the latest commit information
            commits_url = repo["commits_url"].replace('{/sha}', '')  # Remove the placeholder
            commits_response = requests.get(commits_url)

            if commits_response.status_code == 200:
                commits = commits_response.json()
                # Count the number of commits (pushes)
                pushes_count.append(len(commits))

                if commits:  # Check if there are any commits
                    latest_commit = commits[0]  # Get the latest commit
                    last_commits.append({
                        "sha": latest_commit["sha"],
                        "message": latest_commit["commit"]["message"]
                    })
                else:
                    last_commits.append({"sha": None, "message": None})  # No commits found
            else:
                last_commits.append({"sha": None, "message": None})  # Handle commit fetch error
                pushes_count.append(0)  # No pushes if commit fetch fails

        return repos_list, repos_dates, last_commits, pushes_count  # Return repos, dates, last commits, and pushes count
    else:
        return None, None, None, None  # Handle error case


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/github")
def github_page():
    return render_template("github.html")


@app.route("/github/submit", methods=["POST"])
def github_submit():
    input_name = request.form.get("username")
    repositories, dates, last_commits, pushes_count = make_request(input_name)
    repo_data = zip(repositories, dates, last_commits, pushes_count)  # Combine names and dates into pairs
    return render_template("github_hello.html",
                           username=input_name, repo_data=repo_data)


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
            if round(num**(1/2))**2 == num:
                if round(num**(1/3))**3 == num:
                    correct.append(num)
        return ', '.join(str(e) for e in correct)
    elif "power" in string:
        numbers = re.findall(r"\d+", string)
        numbers = [int(num) for num in numbers]
        answer = str(numbers[0]**numbers[1])
        return answer
    elif "minus" in string:
        numbers = re.findall(r"\d+", string)
        numbers = [int(num) for num in numbers]
        answer = str(numbers[0] - numbers[1])
        return answer
    else:
        return "Query not found"


if __name__ == "__main__":
    app.run(debug=True)
