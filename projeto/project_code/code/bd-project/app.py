# from flask import Flask, flash, make_response, render_template, render_template_string, request

# from bd_project import music
# from bd_project import composer
# from bd_project import editor
# from bd_project import score
# from bd_project import warehouse
# from bd_project import arranger
# from bd_project.music import Music
# from bd_project.composer import Composer
# from bd_project.editor import Editor
# from bd_project.score import Score
# from bd_project.warehouse import Warehouse
# from bd_project.arranger import Arranger

# app = Flask(__name__)


# @app.route("/")
# def base():
#     musics = music.list_allMusic()
#     return render_template("index.html", musics=musics)


# @app.route("/music-list", methods=["GET"])
# def music_list():
#     musics = music.list_allMusic()
#     return render_template("music_list.html", musics=musics)


# @app.route("/music-search", methods=["GET"])
# def music_search():
#     query = request.args.get('query', '')
#     musics = music.search_music(query)
#     return render_template("music_list.html", musics=musics)


# @app.route("/music-create", methods=["POST"])
# def new_music_create():
#     new_details = Music(**request.form)
#     music.create(new_details)

#     try:
#         music.create_music(new_details)
#         response = make_response(render_template_string(f"Customer {new_details.title} created successfully!"))
#         response.headers["HX-Trigger"] = "refreshContactList"
#         flash("Music created successfully!")
#     except ValueError as e:
#         response = make_response(render_template_string(f"Error: {e}"))
#         flash(f"Error: {e}")

#     return response


# @app.route("/composer-list", methods=["GET"])
# def composer_list():
#     composers = composer.list_Composers()
#     return render_template("composer_list.html", composers=composers)


# @app.route("/composer-search", methods=["GET"])
# def composer_search():
#     query = request.args.get('query', '')
#     composers = composer.search_composer(query)
#     return render_template("composer_list.html", composers=composers)

# @app.route("/editor-list", methods=["GET"])
# def editor_list():
#     editors = editor.list_editor()
#     return render_template("editor_list.html", editors=editors)

# @app.route("/editor-search", methods=["GET"])
# def editor_search():
#     query = request.args.get('query', '')
#     editors = editor.search_editor(query)
#     return render_template("editor_list.html", editors=editors)


# @app.route("/score-list", methods=["GET"])
# def score_list():
#     scores = score.list_allScores()
#     return render_template("scores_list.html", scores=scores)


# @app.route("/score-search", methods=["GET"])
# def score_search():
#     query = request.args.get('query', '')
#     scores = score.search_score(query)
#     return render_template("scores_list.html", scores=scores)


# @app.route("/warehouse-list", methods=["GET"])
# def warehouse_list():
#     warehouses = warehouse.list_warehouse()
#     return render_template("warehouse_list.html", warehouses=warehouses)


# @app.route("/warehouse-search", methods=["GET"])
# def warehouse_search():
#     query = request.args.get('query', '')
#     warehouses = warehouse.search_warehouse(query)
#     return render_template("warehouse_list.html", warehouses=warehouses)

# @app.route("/arranger-list", methods=["GET"])
# def arranger_list():
#     arrangers = arranger.list_arranger()
#     return render_template("arranger_list.html", arrangers=arrangers)


# @app.route("/arranger-search", methods=["GET"])
# def arranger_search():
#     query = request.args.get('query', '')
#     arrangers = arranger.search_arranger(query)
#     return render_template("arranger_list.html", arrangers=arrangers)
    

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, flash, make_response, render_template, render_template_string, request, redirect, url_for

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
app.secret_key = 'supersecretkey'  # Necessário para usar o flash


@app.route("/")
def base():
    musics = music.list_allMusic()
    return render_template("index.html", musics=musics)

@app.route("/")
def base1():
    composers = composer.list_Composers()
    return render_template("index.html", composers=composers)


@app.route("/music-list", methods=["GET"])
def music_list():
    musics = music.list_allMusic()
    return render_template("music_list.html", musics=musics)


@app.route("/music-search", methods=["GET"])
def music_search():
    query = request.args.get('query', '')
    musics = music.search_music(query)
    return render_template("music_list.html", musics=musics)


@app.route("/music-create", methods=["GET", "POST"])
def new_music_create():
    if request.method == "POST":
        title = request.form.get("title")
        year = request.form.get("year")
        genre_name = request.form.get("genre_name")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        new_details = Music(0, title, int(year), genre_name, fname, lname)

        try:
            music.create_music(new_details)
            flash("Music created successfully!")
            return redirect(url_for('base'))  # Redirecionar para a página principal
        except ValueError as e:
            return render_template("music_create.html", genres=music.list_genres(), error=str(e))
        
    genres = music.list_genres()
    return render_template("music_create.html", genres=genres)


@app.route("/music-delete/<int:music_id>", methods=["POST"])
def delete_music(music_id):
    try:
        music.delete_music(music_id)
        flash("Music deleted successfully!")
    except Exception as e:
        flash(f"Failed to delete music: {e}")
    return redirect(url_for('base'))


@app.route("/composer-list", methods=["GET"])
def composer_list():
    composers = composer.list_Composers()
    return render_template("composer_list.html", composers=composers)


@app.route("/composer-search", methods=["GET"])
def composer_search():
    query = request.args.get('query', '')
    composers = composer.search_composer(query)
    return render_template("composer_list.html", composers=composers)

@app.route("/composer-create", methods=["GET", "POST"])
def new_composer_create():
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        genre = request.form.get("genre")
        birthYear = request.form.get("birthYear")
        deathYear = request.form.get("deathYear")
        genre_name = request.form.get("genre_name")

        new_details = Composer(0, fname, lname, genre, birthYear, deathYear, genre_name)

        try:
            composer.create_composer(new_details)
            flash("Composer created successfully!")
            return redirect(url_for('base1'))  # Redirecionar para a página principal
        except ValueError as e:
            return render_template("composer_create.html", genres=composer.list_genres(), error=str(e))
        
    genres = composer.list_genres()
    return render_template("composer_create.html", genres=genres)

@app.route("/editor-list", methods=["GET"])
def editor_list():
    editors = editor.list_editor()
    return render_template("editor_list.html", editors=editors)

@app.route("/editor-search", methods=["GET"])
def editor_search():
    query = request.args.get('query', '')
    editors = editor.search_editor(query)
    return render_template("editor_list.html", editors=editors)

@app.route("/editor-create", methods=["GET", "POST"])
def new_editor_create():
    if request.method == "POST":
        name = request.form.get("name")
        location = request.form.get("location")

        new_details = Editor(name, 0, location)

        try:
            editor.create_editor(new_details)
            flash("Editor created successfully!")
            return redirect(url_for('base'))  # Redirecionar para a página principal
        except ValueError as e:
            return render_template("editor_create.html", error=str(e))
        
    return render_template("editor_create.html")


@app.route("/score-list", methods=["GET"])
def score_list():
    scores = score.list_allScores()
    return render_template("scores_list.html", scores=scores)


@app.route("/score-search", methods=["GET"])
def score_search():
    query = request.args.get('query', '')
    scores = score.search_score(query)
    return render_template("scores_list.html", scores=scores)

@app.route("/score-create", methods=["GET", "POST"])
def new_score_create():
    if request.method == "POST":
        edition = request.form.get("edition")
        price = request.form.get("price")
        availability = request.form.get("availability")
        difficultyGrade = request.form.get("difficultyGrade")
        editor_name = request.form.get("editor_name")
        music = request.form.get("music")
        new_details = Score(0, edition, price, availability, difficultyGrade, music, editor_name)

        try:
            score.create_score(new_details)
            flash("Score created successfully!")
            return redirect(url_for('base'))  # Redirecionar para a página principal
        except ValueError as e:
            return render_template("score_create.html", editors=score.list_editors(), musics=score.list_musics(), error=str(e))
        
    editors = score.list_editors()
    musics = score.list_musics()
    return render_template("score_create.html", editors=editors, musics=musics)


@app.route("/warehouse-list", methods=["GET"])
def warehouse_list():
    warehouses = warehouse.list_warehouse()
    return render_template("warehouse_list.html", warehouses=warehouses)


@app.route("/warehouse-search", methods=["GET"])
def warehouse_search():
    query = request.args.get('query', '')
    warehouses = warehouse.search_warehouse(query)
    return render_template("warehouse_list.html", warehouses=warehouses)

@app.route("/warehouse-create", methods=["GET", "POST"])
def new_warehouse_create():
    if request.method == "POST":
        name = request.form.get("name")
        storage = request.form.get("storage")
        editor_name = request.form.get("editor_name")
        new_details = Warehouse(name, 0, storage, editor_name)

        try:
            warehouse.create_warehouse(new_details)
            flash("Warehouse created successfully!")
            return redirect(url_for('base'))  # Redirecionar para a página principal
        except ValueError as e:
            return render_template("warehouse_create.html", editors=warehouse.list_editors(), error=str(e))
        
    editors = warehouse.list_editors()
    return render_template("warehouse_create.html", editors=editors)

@app.route("/arranger-list", methods=["GET"])
def arranger_list():
    arrangers = arranger.list_arranger()
    return render_template("arranger_list.html", arrangers=arrangers)


@app.route("/arranger-search", methods=["GET"])
def arranger_search():
    query = request.args.get('query', '')
    arrangers = arranger.search_arranger(query)
    return render_template("arranger_list.html", arrangers=arrangers)

@app.route("/arranger-create", methods=["GET", "POST"])
def new_arranger_create():
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        genre = request.form.get("genre")
        birthYear = request.form.get("birthYear")
        deathYear = request.form.get("deathYear")
        genre_name = request.form.get("genre_name")

        new_details = Arranger(0, fname, lname, genre, birthYear, deathYear, genre_name)

        try:
            arranger.create_arranger(new_details)
            flash("Arranger created successfully!")
            return redirect(url_for('base'))  # Redirecionar para a página principal
        except ValueError as e:
            return render_template("arranger_create.html", genres=arranger.list_genres(), error=str(e))
        
    genres = arranger.list_genres()
    return render_template("arranger_create.html", genres=genres)
    

if __name__ == "__main__":
    app.run(debug=True)
