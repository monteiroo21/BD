from bd_project.session import create_connection
from flask import Flask, flash, render_template, request, redirect, url_for

from bd_project import customer, music, composer, editor, score, warehouse, arranger, transaction
from bd_project.music import Music
from bd_project.composer import Composer
from bd_project.editor import Editor
from bd_project.score import Score
from bd_project.warehouse import Warehouse
from bd_project.arranger import Arranger
from bd_project.customer import Customer
from bd_project.transaction import Transaction
from bd_project.statistics import get_composer_revenue, get_genre_sales, get_composition_count_by_composer, get_music_sales_by_genre


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
        composer = request.form.get("composer")
        new_details = Music(0, title, int(year), genre_name, composer)

        try:
            music.create_music(new_details)
            flash("Music created successfully!")
            return redirect(url_for('base'))
        except ValueError as e:
            flash(f"Error: {e}")
            return redirect(url_for('base'))
        
    genres = music.list_genres()
    composers = music.list_composers()
    return render_template("music_create.html", genres=genres, composers=composers)


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
        composer = request.form.get("composer")
        new_details = Music(music_id, title, int(year), genre_name, composer)

        try:
            music.edit_music(new_details)
            flash("Music edited successfully!")
            return redirect(url_for('base'))
        except ValueError as e:
            flash(f"Error: {e}")
            return redirect(url_for('base'))
    else:
        current_music = music.get_music_by_id(music_id)

        if current_music is None:
            flash("Music not found", "error")
            return redirect(url_for('base'))
        
        genres = music.list_genres()
        composers = music.list_composers()
        return render_template("music_edit.html", genres=genres, composers=composers, music=current_music)
    

@app.route("/deleted-musics", methods=["GET"])
def view_deleted_musics():
    deleted_musics = music.get_deleted_musics()
    return render_template("deleted_musics.html", deleted_musics=deleted_musics)
    

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

        if deathYear == "":
            deathYear = None

        new_details = Composer(0, fname, lname, genre, birthYear, deathYear, genre_name)

        try:
            composer.create_composer(new_details)
            flash("Composer created successfully!")
            return redirect(url_for('base'))
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

        if death_year == "":
            death_year = None

        current_composer = composer.get_composer_by_id(composer_id)
        if current_composer is None:
            flash("Composer not found", "error")
            return redirect(url_for('base'))

        new_details = Composer(composer_id, fname, lname, genre, birth_year, death_year, genre_name)

        try:
            composer.edit_composer(new_details, current_composer.Fname, current_composer.Lname)
            flash("Composer edited successfully!")
            return redirect(url_for('base'))
        except Exception as e:
            flash(f"Error: {e}")
            return redirect(url_for('base'))
    else:
        current_composer = composer.get_composer_by_id(composer_id)

        if current_composer is None:
            flash("Composer not found", "error")
            return redirect(url_for('base'))
        
        genres = composer.list_genres()
        return render_template("composer_edit.html", genres=genres, composer=current_composer)
    

@app.route("/composer-details/<int:composer_id>", methods=["GET"])
def detail_composer(composer_id):
    composer_details = composer.detail_composer(composer_id)
    return render_template("composer_details.html", composer=composer_details)


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
            return redirect(url_for('base'))
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
            current_editor = editor.get_editor_by_id(editor_id)
            
            if current_editor is None:
                flash("Editor not found", "error")
                return redirect(url_for('base'))
            
            editor.edit_editor(current_editor.name, name, location)
            flash("Editor edited successfully!")
            return redirect(url_for('base'))
        except ValueError as e:
            flash(f"Error: {e}")
            return redirect(url_for('base'))
    else:
        current_editor = editor.get_editor_by_id(editor_id)

        if current_editor is None:
            flash("Editor not found", "error")
            return redirect(url_for('base'))
        
        return render_template("editor_edit.html", editor=current_editor)
    

@app.route("/editor-details/<int:editor_id>", methods=["GET"])
def detail_editor(editor_id):
    editor_details = editor.detail_editor(editor_id)
    return render_template("editor_details.html", editor=editor_details)


@app.route("/score-list", methods=["GET"])
def score_list():
    scores = score.list_allScores()
    return render_template("scores_list.html", scores=scores)


@app.route("/score-search", methods=["GET"])
def search_score():
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
        new_details = Score(0, edition, price, availability, difficultyGrade, music, editor_name, arranger, type)

        try:
            score.create_score(new_details)
            flash("Score created successfully!")
            return redirect(url_for('base'))  # Redirecionar para a página principal
        except ValueError as e:
            return render_template("score_create.html", editors=score.list_editors(), musics=score.list_musics(), arrangers=score.list_arrangers(), error=str(e))
        
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

        new_details = Score(register_num, edition, price, availability, difficultyGrade, music, editor_name, arranger, type)

        try:
            score.edit_score(new_details)
            flash("Score edited successfully!")
            return redirect(url_for('base'))  # Redirect to the main page
        except ValueError as e:
            return render_template("score_edit.html", editors=score.list_editors(), musics=score.list_musics(), arrangers=score.list_arrangers(), error=str(e), score=new_details)
        
    else:
        current_score = score.get_score_by_id(register_num)

        if current_score is None:
            flash("Score not found", "error")
            return redirect(url_for('base'))

        editors = score.list_editors()
        musics = score.list_musics()
        arrangers = score.list_arrangers()
        return render_template("score_edit.html", editors=editors, musics=musics, arrangers=arrangers, score=current_score)

@app.route("/score-list-sorted", methods=["GET"])
def score_list_sorted():
    scores = score.filter_scores_by_price()
    return render_template("scores_list.html", scores=scores)

@app.route("/score-details/<int:register_num>", methods=["GET"])
def detail_score(register_num):
    score_details = score.detail_score(register_num)
    return render_template("score_details.html", score=score_details)

@app.route("/add-instrumentation/<int:register_num>", methods=["GET", "POST"])
def add_instrumentation(register_num):
    if request.method == "POST":
        instrument = request.form.get("instrument")
        quantity = request.form.get("quantity")
        family = request.form.get("family")
        role = request.form.get("role")

        try:
            score.add_instrumentation(instrument, quantity, family, role, register_num)
            flash("Instrumentation added successfully!")
            return redirect(url_for('base', register_num=register_num))
        except Exception as e:
            flash(f"Error: {e}")
            return redirect(url_for('base', register_num=register_num))

    else:
        score_details = score.detail_score(register_num)
        if score_details is None:
            flash("Score not found", "error")
            return redirect(url_for('base'))
        
        return render_template("add_instrumentation.html", score=score_details)


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
            return redirect(url_for('base'))
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

        if deathYear == "":
            deathYear = None

        new_details = Arranger(0, fname, lname, genre, birthYear, deathYear, genre_name)

        try:
            arranger.create_arranger(new_details)
            flash("Arranger created successfully!")
            return redirect(url_for('base'))
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

        if death_year == "":
            death_year = None

        current_arranger = arranger.get_arranger_by_id(arranger_id)
        if current_arranger is None:
            flash("Arranger not found", "error")
            return redirect(url_for('base'))

        new_details = Arranger(arranger_id, fname, lname, genre, birth_year, death_year, genre_name)

        try:
            arranger.edit_arranger(new_details, current_arranger.fname, current_arranger.lname)
            flash("Arranger edited successfully!")
            return redirect(url_for('base'))
        except ValueError as e:
            flash(f"Error: {e}")
            return redirect(url_for('base'))
    else:
        current_arranger = arranger.get_arranger_by_id(arranger_id)

        if current_arranger is None:
            flash("Arranger not found", "error")
            return redirect(url_for('base'))
        
        genres = arranger.list_genres()
        return render_template("arranger_edit.html", genres=genres, arranger=current_arranger)
    
@app.route("/arranger-details/<int:arranger_id>", methods=["GET"])
def detail_arranger(arranger_id):
    arranger_details = arranger.detail_arranger(arranger_id)
    return render_template("arranger_details.html", arranger=arranger_details)


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
            flash(f"Error: {e}")
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


@app.route("/customer-edit/<int:numCC>", methods=["GET", "POST"])
def edit_customer_route(numCC):
    if request.method == "POST":
        email_address = request.form.get("email_address")
        numBankAccount = request.form.get("numBankAccount")
        cellNumber = request.form.get("cellNumber")
        name = request.form.get("name")
        
        try:
            customer.edit_customer(numCC, name, email_address, numBankAccount, cellNumber)
            flash("Customer edited successfully!")
            return redirect(url_for('base'))
        except ValueError as e:
            flash(f"Error: {e}")
            return redirect(url_for('base'))
    else:
        current_customer = customer.detail_customer(numCC)

        if current_customer is None:
            flash("Customer not found", "error")
            return redirect(url_for('base'))

        return render_template("customer_edit.html", customer=current_customer)


@app.route("/customer-details/<int:numCC>", methods=["GET"])
def detail_customer_route(numCC):
    try:
        customer_details = customer.detail_customer(numCC)
        return render_template("customer_details.html", customer=customer_details)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for('customer_list'))


@app.route("/transaction-list", methods=["GET"])
def transaction_list():
    transactions = transaction.list_transactions()
    return render_template("transaction_list.html", transactions=transactions)


@app.route("/transaction-search", methods=["GET"])
def transaction_search():
    query = request.args.get('query', '')
    transactions = transaction.search_transaction(query)
    return render_template("transaction_list.html", transactions=transactions)


@app.route("/transaction-create", methods=["GET", "POST"])
def transaction_create():
    if request.method == "POST":
        customer_id = request.form.get("customer")
        scores = request.form.getlist("scores")
        date = request.form.get("date")
        
        transaction_id = get_new_transaction_id()
        
        # Calculate the total value of the selected scores
        total_value = 0
        for score_id in scores:
            score_details = score.get_score_by_id(int(score_id))
            total_value += score_details.price
        
        transaction_data = Transaction(transaction_id, total_value, date, int(customer_id))

        try:
            transaction.create_transaction(transaction_data, [int(score) for score in scores])
            flash("Transaction created successfully!")
            return redirect(url_for("transaction_list"))
        except Exception as e:
            flash(f"Error: {e}")
            return redirect(url_for("base"))
    
    customers = transaction.list_customers()
    scores = transaction.list_scores()
    return render_template("transaction_create.html", customers=customers, scores=scores)


def get_new_transaction_id():
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COALESCE(MAX(transaction_id), 0) + 1 FROM [Transaction]")
            return cursor.fetchone()[0]


@app.route("/new-transaction/<int:customer_id>", methods=["GET", "POST"])
def new_transaction(customer_id):
    if request.method == "POST":
        scores = request.form.get("selected_scores").split(',')
        date = request.form.get("date")
        
        transaction_id = get_new_transaction_id()
        
        total_value = 0
        for score_id in scores:
            score_details = score.get_score_by_id(int(score_id))
            total_value += score_details.price
        
        transaction_data = Transaction(transaction_id, total_value, date, customer_id)

        try:
            transaction.create_transaction(transaction_data, [int(score) for score in scores])
            flash("Transaction created successfully!")
            return redirect(url_for("base"))
        except Exception as e:
            flash(f"Error: {e}")
            return redirect(url_for("customer_details", numCC=customer_id))
    
    customer_details = customer.detail_customer(customer_id)
    scores = customer.list_all_scores_with_details()
    return render_template("new_transaction.html", customer=customer_details, scores=scores)


@app.route("/statistics", methods=["GET"])
def statistics():
    composer_revenue = get_composer_revenue()
    genre_sales = get_genre_sales()
    composition_count = get_composition_count_by_composer()  # Adicionado
    music_sales = get_music_sales_by_genre()  # Adicionado
    return render_template("statistics_page.html", composer_revenue=composer_revenue, genre_sales=genre_sales, composition_count=composition_count, music_sales=music_sales)  # Atualizado


if __name__ == "__main__":
    app.run(debug=True)
