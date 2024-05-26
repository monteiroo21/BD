from bd_project.session import create_connection
from flask import Flask, flash, make_response, render_template, render_template_string, request, redirect, url_for

from bd_project import customer, music
from bd_project import composer
from bd_project import editor
from bd_project import score
from bd_project import warehouse
from bd_project import arranger
from bd_project import transaction
from bd_project.music import Music
from bd_project.composer import Composer
from bd_project.editor import Editor
from bd_project.score import Score
from bd_project.warehouse import Warehouse
from bd_project.arranger import Arranger
from bd_project.customer import Customer
from bd_project.transaction import Transaction


app = Flask(__name__)
app.secret_key = 'supersecretkey'


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
    

####################################################################


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
            return redirect(url_for('base'))  # Redirecionar para a página principal
        except ValueError as e:
            print(f"Error: {e}")
            return redirect(url_for('base'))
        
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


@app.route("/composer-edit/<int:composer_id>", methods=["GET", "POST"])
def edit_composer_route(composer_id):
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        genre = request.form.get("genre")
        birth_year = request.form.get("birthYear")
        death_year = request.form.get("deathYear")
        genre_name = request.form.get("genre_name")

        # Fetch the current composer details
        current_composer = composer.get_composer_by_id(composer_id)
        if current_composer is None:
            flash("Composer not found", "error")
            return redirect(url_for('base'))

        # Create a Composer object with the new details
        new_details = Composer(composer_id, fname, lname, genre, birth_year, death_year, genre_name)

        try:
            # Call the edit_composer function to update the composer record
            composer.edit_composer(new_details, current_composer.Fname, current_composer.Lname)
            flash("Composer edited successfully!")
            return redirect(url_for('base'))
        except ValueError as e:
            flash(f"Error: {e}")
            return redirect(url_for('base'))
    else:
        # Fetch the current composer details for the GET request
        current_composer = composer.get_composer_by_id(composer_id)

        if current_composer is None:
            flash("Composer not found", "error")
            return redirect(url_for('base'))
        
        # Fetch the list of genres for the dropdown menu in the form
        genres = composer.list_genres()
        return render_template("composer_edit.html", genres=genres, composer=current_composer)
    

@app.route("/composer-details/<int:composer_id>", methods=["GET"])
def detail_composer(composer_id):
    composer_details = composer.detail_composer(composer_id)
    return render_template("composer_details.html", composer=composer_details)


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
    
@app.route("/editor-details/<int:editor_id>", methods=["GET"])
def detail_editor(editor_id):
    editor_details = editor.detail_editor(editor_id)
    return render_template("editor_details.html", editor=editor_details)

################################################################################


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
        arranger = request.form.get("arranger")
        type = request.form.get("type")

        instrumentations = []
        instruments = request.form.getlist("instrument[]")
        quantities = request.form.getlist("quantity[]")
        families = request.form.getlist("family[]")
        roles = request.form.getlist("role[]")

        for instrument, quantity, family, role in zip(instruments, quantities, families, roles):
            instrumentations.append(score.Instrumentation(instrument, int(quantity), family, role))

        new_details = score.Score(0, int(edition), float(price), int(availability), int(difficultyGrade), music, editor_name, arranger, type)

        try:
            score.create_score(new_details, instrumentations)
            flash("Score created successfully!")
            return redirect(url_for('base'))
        except ValueError as e:
            return render_template("score_create.html", editors=score.list_editors(), musics=score.list_musics(), error=str(e))

    editors = score.list_editors()
    musics = score.list_musics()
    arrangers = score.list_arrangers()
    return render_template("score_create.html", editors=editors, musics=musics, arrangers=arrangers)



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

@app.route("/score-edit/<int:register_num>", methods=["GET", "POST"])
def edit_score_route(register_num):
    if request.method == "POST":
        edition = request.form.get("edition")
        price = request.form.get("price")
        availability = request.form.get("availability")
        difficultyGrade = request.form.get("difficultyGrade")
        editor_name = request.form.get("editor_name")
        music = request.form.get("music")
        arranger = request.form.get("arranger")
        type = request.form.get("type")

        instrumentations = []
        instruments = request.form.getlist("instrument[]")
        quantities = request.form.getlist("quantity[]")
        families = request.form.getlist("family[]")
        roles = request.form.getlist("role[]")

        for instrument, quantity, family, role in zip(instruments, quantities, families, roles):
            instrumentations.append(score.Instrumentation(instrument, int(quantity), family, role))

        updated_details = score.Score(register_num, int(edition), float(price), int(availability), int(difficultyGrade), music, editor_name, arranger, type)

        try:
            score.edit_score(updated_details, instrumentations)
            flash("Score updated successfully!")
            return redirect(url_for('base'))
        except ValueError as e:
            return render_template("score_edit.html", score=updated_details, instrumentations=instrumentations, editors=score.list_editors(), musics=score.list_musics(), error=str(e))

    score_details = score.get_score_by_id(register_num)
    instrumentations = score.get_instrumentations_by_score_id(register_num)
    editors = score.list_editors()
    musics = score.list_musics()
    arrangers = score.list_arrangers()
    return render_template("score_edit.html", score=score_details, instrumentations=instrumentations, editors=editors, musics=musics, arrangers=arrangers)
    

@app.route("/score-list-sorted", methods=["GET"])
def score_list_sorted():
    scores = score.filter_scores_by_price()
    return render_template("scores_list.html", scores=scores)



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
        location = request.form.get("location")
        new_details = Warehouse(name, 0, storage, editor_name, location)
        

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
        location = request.form.get("location")

        new_details = Warehouse(name, warehouse_id, storage, editor_name, location)

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
    

@app.route("/warehouse-details/<int:warehouse_id>", methods=["GET"])
def detail_warehouse(warehouse_id):
    warehouse_details = warehouse.detail_warehouse(warehouse_id)
    return render_template("warehouse_details.html", warehouse=warehouse_details)



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


@app.route("/arranger-edit/<int:arranger_id>", methods=["GET", "POST"])
def edit_arranger_route(arranger_id):
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        genre = request.form.get("genre")
        birth_year = request.form.get("birthYear")
        death_year = request.form.get("deathYear")
        genre_name = request.form.get("genre_name")

        # Fetch the current arranger details
        current_arranger = arranger.get_arranger_by_id(arranger_id)
        if current_arranger is None:
            flash("Arranger not found", "error")
            return redirect(url_for('base'))

        # Create a Arranger object with the new details
        new_details = Arranger(arranger_id, fname, lname, genre, birth_year, death_year, genre_name)

        try:
            # Call the edit_arranger function to update the arranger record
            arranger.edit_arranger(new_details, current_arranger.fname, current_arranger.lname)
            flash("Arranger edited successfully!")
            return redirect(url_for('base'))
        except ValueError as e:
            flash(f"Error: {e}")
            return redirect(url_for('base'))
    else:
        # Fetch the current arranger details for the GET request
        current_arranger = arranger.get_arranger_by_id(arranger_id)

        if current_arranger is None:
            flash("Arranger not found", "error")
            return redirect(url_for('base'))
        
        # Fetch the list of genres for the dropdown menu in the form
        genres = arranger.list_genres()
        return render_template("arranger_edit.html", genres=genres, arranger=current_arranger)
    
@app.route("/arranger-details/<int:arranger_id>", methods=["GET"])
def detail_arranger(arranger_id):
    arranger_details = arranger.detail_arranger(arranger_id)
    return render_template("arranger_details.html", arranger=arranger_details)

####################################################################

@app.route("/customer-list", methods=["GET"])
def customer_list():
    customers = customer.list_customers_with_transaction_count()
    return render_template("customer_list.html", customers=customers)


@app.route("/customer-search", methods=["GET"])
def customer_search():
    query = request.args.get('query', '')
    customers = customer.search_customer_with_transaction_count(query)
    return render_template("customer_list.html", customers=customers)


@app.route("/customer-create", methods=["GET", "POST"])
def new_customer_create():
    if request.method == "POST":
        numCC = request.form.get("numCC")
        email_address = request.form.get("email_address")
        numBankAccount = request.form.get("numBankAccount")
        cellNumber = request.form.get("cellNumber")
        name = request.form.get("name")
        new_details = Customer(numCC, email_address, numBankAccount, cellNumber, name)

        try:
            customer.create_customer(new_details)
            flash("Customer created successfully!")
            return redirect(url_for('base'))
        except Exception as e:
            print(f"Error: {e}")
            return redirect(url_for('base'))
        
    return render_template("customer_create.html")


@app.route("/customer-delete/<int:numCC>", methods=["POST"])
def delete_customer_route(numCC):
    try:
        customer.delete_customer(numCC)
        flash("Customer deleted successfully!")
    except Exception as e:
        flash(str(e))
    return redirect(url_for('base'))


####################################################################

@app.route("/transaction-list", methods=["GET"])
def transaction_list():
    transactions = transaction.list_transactions()
    return render_template("transaction_list.html", transactions=transactions)


@app.route("/transaction-search", methods=["GET"])
def transaction_search():
    query = request.args.get('query', '')
    transactions = transaction.search_transaction(query)
    return render_template("transaction_list.html", transactions=transactions)





if __name__ == "__main__":
    app.run(debug=True)
