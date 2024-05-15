from flask import Flask, make_response, render_template, render_template_string, request

from bd_project import writers


app = Flask(__name__)


@app.route("/")
def base():
    writers_list = writers.list_all()
    return render_template("index.html", writers=writers_list)


@app.route("/writer-list", methods=["GET"])
def writer_list():
    writers_list = writers.list_all()
    return render_template("writer_list.html", writers=writers_list)
    

if __name__ == "__main__":
    app.run(debug=True)
