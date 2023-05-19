import json
from dataclasses import dataclass

from flask import Flask, jsonify, redirect, request, url_for

app = Flask(__name__, static_folder=".", static_url_path="")


@dataclass
class TodoRecord:
    checked: bool
    title: str
    description: str

    def json(self) -> str:
        return json.dumps(self)


def make_todo_record(form) -> TodoRecord:
    return TodoRecord(form.get("checked", "") == "on", form.get("title", ""), form.get("description", ""))


def data2html(record: TodoRecord, id: int) -> str:
    return f"""
        <div class="todo-item-wrap">
            <input type="checkbox" name="completed[]" value="{id}" {"checked" if record.checked else ""} />
            <div class="todo-details-wrap">
                <h2>{record.title}</h2>
                <p>{record.description}</p>
            </div>
        </div>
    """


data = {}


@app.route("/")
def index():
    return f"""
        <!DOCTYPE html>
        <html lang="ja">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Index | Todo-list</title>
                <style>
                    #todos-wrap {{
                        display: flex;
                        flex-direction: column;
                    }}
                    .todo-item-wrap {{
                        display: flex;
                        align-items: flex-start;
                        margin-block: 1rem;
                    }}
                    .todo-details-wrap {{
                        margin: 0;
                    }}
                    .todo-item-wrap h2 {{
                        font-size: 1.2rem;
                        margin: 0;
                    }}
                    .todo-item-wrap p {{
                        margin: 0;
                    }}
                </style>
            </head>
            <body>
                <h1>Todoリスト</h1>
                <form method="POST" action="/edit">
                    <div id="todos-wrap">
                        {" ".join(map(lambda i: data2html(data[i], i), data))}
                    </div>
                    <input type="submit" name="更新" />
                </form>
                <a href="/append">
                    <button type="button">新規作成</button>
                </a>
            </body>
        </html>
    """


@app.route("/append", methods=["GET", "POST"])
def append():
    if request.method == "POST":
        new_record = make_todo_record(request.form)
        data[len(data)] = new_record
        return redirect(url_for("index"))
    return """
        <!DOCTYPE html>
        <html lang="ja">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Append | Todo-list</title>
            </head>
            <body>
                <h1>Todoリスト</h1>
                <form method="POST" action="/append">
                    <label>
                        タイトル
                        <input name="title" />
                    </label>
                    <label>
                        説明文
                        <input name="description" />
                    </label>
                    <input type="submit" name="更新" />
                </form>
            </body>
        </html>
    """


@app.route("/edit", methods=["POST"])
def edit():
    try:
        checkeds = {i: False for i in data.keys()}
        req_checkeds = request.form.getlist("completed[]")
        for i in req_checkeds:
            print(i)
            checkeds[int(i)] = True
        for i, checked in checkeds.items():
            data[i].checked = checked
        return redirect(url_for("index"))
    except:
        return jsonify({"message": "invalid id"}), 400


app.run(port=8080, debug=True)
