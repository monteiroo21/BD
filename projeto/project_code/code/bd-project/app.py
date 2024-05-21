from flask import Flask, make_response, render_template, render_template_string, request

from bd_project import music
from bd_project import composer
from bd_project import editor
from bd_project import score
from bd_project import warehouse
from bd_project import arranger
from bd_project.music import Music
from bd_project.composer import Composer
from bd_project.editor import Editor
from bd_project.score import Score
from bd_project.warehouse import Warehouse
from bd_project.arranger import Arranger

app = Flask(__name__)


@app.route("/")
def base():
    musics = music.list_allMusic()
    return render_template("index.html", musics=musics)


@app.route("/music-list", methods=["GET"])
def music_list():
    musics = music.list_allMusic()
    return render_template("music_list.html", musics=musics)


@app.route("/music-search", methods=["GET"])
def music_search():
    query = request.args.get('query', '')
    musics = music.search_music(query)
    return render_template("music_list.html", musics=musics)


@app.route("/composer-list", methods=["GET"])
def composer_list():
    composers = composer.list_Composers()
    return render_template("composer_list.html", composers=composers)


@app.route("/composer-search", methods=["GET"])
def composer_search():
    query = request.args.get('query', '')
    composers = composer.search_composer(query)
    return render_template("composer_list.html", composers=composers)

@app.route("/editor-list", methods=["GET"])
def editor_list():
    editors = editor.list_editor()
    return render_template("editor_list.html", editors=editors)

@app.route("/editor-search", methods=["GET"])
def editor_search():
    query = request.args.get('query', '')
    editors = editor.search_editor(query)
    return render_template("editor_list.html", editors=editors)


@app.route("/score-list", methods=["GET"])
def score_list():
    scores = score.list_allScores()
    return render_template("scores_list.html", scores=scores)


@app.route("/score-search", methods=["GET"])
def score_search():
    query = request.args.get('query', '')
    scores = score.search_score(query)
    return render_template("scores_list.html", scores=scores)


@app.route("/warehouse-list", methods=["GET"])
def warehouse_list():
    warehouses = warehouse.list_warehouse()
    return render_template("warehouse_list.html", warehouses=warehouses)


@app.route("/warehouse-search", methods=["GET"])
def warehouse_search():
    query = request.args.get('query', '')
    warehouses = warehouse.search_warehouse(query)
    return render_template("warehouse_list.html", warehouses=warehouses)

@app.route("/arranger-list", methods=["GET"])
def arranger_list():
    arrangers = arranger.list_arranger()
    return render_template("arranger_list.html", arrangers=arrangers)


@app.route("/arranger-search", methods=["GET"])
def arranger_search():
    query = request.args.get('query', '')
    arrangers = arranger.search_arranger(query)
    return render_template("arranger_list.html", arrangers=arrangers)
    

if __name__ == "__main__":
    app.run(debug=True)
