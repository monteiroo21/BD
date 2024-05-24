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
from bd_project.music import MusicDetails


app = Flask(__name__)
app.secret_key = 'supersecretkey'


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
            return redirect(url_for('base'))
        except ValueError as e:
            flash(f"Error: {e}")
            return redirect(url_for('base'))
        
    genres = music.list_genres()
    return render_template("music_create.html", genres=genres)


# @app.route("/music-details/<int:music_id>", methods=["GET"])
# def detail_music(music_id):
#     music_details = music.detail_music(music_id)
#     return render_template("music_details.html", music_details=music_details)

@app.route("/music-details/<int:music_id>", methods=["GET"])
def detail_music(music_id):
    music_details = music.detail_music(music_id)
    return render_template("music_details.html", music=music_details)


@app.route("/music-delete/<int:music_id>", methods=["POST"])
def delete_music(music_id):
    try:
        music.delete_music(music_id)
        flash("Music deleted successfully!")
    except Exception as e:
        flash(f"Failed to delete music: {e}")
    return redirect(url_for('base'))

@app.route("/music-edit/<int:music_id>", methods=["GET", "POST"])
def edit_music_route(music_id):
    if request.method == "POST":
        title = request.form.get("title")
        year = request.form.get("year")
        genre_name = request.form.get("genre_name")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        
        # Create a Music object with the provided details, including the music_id
        new_details = Music(music_id, title, int(year), genre_name, fname, lname)

        try:
            # Call the edit_music function to update the music record
            music.edit_music(new_details)
            flash("Music edited successfully!")
            return redirect(url_for('base'))
        except ValueError as e:
            flash(f"Error: {e}")
            return redirect(url_for('base'))
    else:
        # Fetch the current music details for the GET request
        current_music = music.get_music_by_id(music_id)  # Assuming this function fetches the music details

        if current_music is None:
            flash("Music not found", "error")
            return redirect(url_for('base'))
        
        # Fetch the list of genres for the dropdown menu in the form
        genres = music.list_genres()
        return render_template("music_edit.html", genres=genres, music=current_music)


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

@app.route("/composer-delete/<int:composer_id>", methods=["POST"])
def delete_composer_route(composer_id):
    try:
        composer.delete_composer(composer_id)
        flash("Composer deleted successfully!")
    except ValueError as e:
        flash(str(e))
    except RuntimeError as e:
        flash(str(e))
    return redirect(url_for('base'))


####################################################################



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


@app.route("/editor-delete/<int:editor_id>", methods=["POST"])
def delete_editor_route(editor_id):
    try:
        editor.delete_editor(editor_id)
        flash("Editor deleted successfully!")
    except ValueError as e:
        flash(str(e))
    except RuntimeError as e:
        flash(str(e))
    return redirect(url_for('base'))


@app.route("/editor-edit/<int:editor_id>", methods=["GET", "POST"])
def edit_editor_route(editor_id):
    if request.method == "POST":
        name = request.form.get("name")
        location = request.form.get("location")

        try:
            # Fetch the current editor details using the editor_id
            current_editor = editor.get_editor_by_id(editor_id)
            
            if current_editor is None:
                flash("Editor not found", "error")
                return redirect(url_for('base'))
            
            # Update editor details
            editor.edit_editor(current_editor.name, name, location)
            flash("Editor edited successfully!")
            return redirect(url_for('base'))
        except ValueError as e:
            flash(f"Error: {e}")
            return redirect(url_for('base'))
    else:
        # Fetch the current editor details for the GET request
        current_editor = editor.get_editor_by_id(editor_id)

        if current_editor is None:
            flash("Editor not found", "error")
            return redirect(url_for('base'))
        
        return render_template("editor_edit.html", editor=current_editor)


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


@app.route("/score-delete/<int:register_num>", methods=["POST"])
def delete_score_route(register_num):
    try:
        score.delete_score(register_num)
        flash("Score deleted successfully!")
    except ValueError as e:
        flash(str(e))
    except RuntimeError as e:
        flash(str(e))
    return redirect(url_for('base'))



####################################################################




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


@app.route("/warehouse-delete/<int:warehouse_id>", methods=["POST"])
def delete_warehouse_route(warehouse_id):
    try:
        warehouse.delete_warehouse(warehouse_id)
        flash("Warehouse deleted successfully!")
    except ValueError as e:
        flash(str(e))
    except RuntimeError as e:
        flash(str(e))
    return redirect(url_for('base'))


@app.route("/warehouse-edit/<int:warehouse_id>", methods=["GET", "POST"])
def edit_warehouse_route(warehouse_id):
    if request.method == "POST":
        name = request.form.get("name")
        storage = request.form.get("storage")
        editor_name = request.form.get("editor_name")

        new_details = Warehouse(name, warehouse_id, storage, editor_name)

        try:
            warehouse.edit_warehouse(new_details)
            flash("Warehouse edited successfully!")
            return redirect(url_for('base'))
        except ValueError as e:
            flash(f"Error: {e}")
            return redirect(url_for('base'))
    else:
        # Fetch the current warehouse details for the GET request
        current_warehouse = warehouse.get_warehouse_by_id(warehouse_id)
        editors = warehouse.list_editors()

        if current_warehouse is None:
            flash("Warehouse not found", "error")
            return redirect(url_for('base'))
        
        return render_template("warehouse_edit.html", warehouse=current_warehouse, editors=editors)



####################################################################




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


@app.route("/arranger-delete/<int:arranger_id>", methods=["POST"])
def delete_arranger_route(arranger_id):
    try:
        arranger.delete_arranger(arranger_id)
        flash("Arranger deleted successfully!")
    except ValueError as e:
        flash(str(e))
    except RuntimeError as e:
        flash(str(e))
    return redirect(url_for('base'))
    

if __name__ == "__main__":
    app.run(debug=True)
