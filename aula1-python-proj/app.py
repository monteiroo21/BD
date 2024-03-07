import pyodbc
from flask import Flask, render_template, request, render_template_string

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test_connection', methods=['POST'])
def test_connection():
    # Get form data
    server_addr = request.form['connection_string']
    db_name = request.form['database_name']
    user = request.form['user']
    password = request.form['password']

    try:
        with create_connection(server_addr, db_name, user, password) as conn:
            message = "Connection successful!"
            colour = "green"
    except pyodbc.Error as e:
        message = f"Connection failed: {str(e)}"
        colour = "red"

    return f'<label style="color: {colour};">{message}</label>'


@app.route('/hello', methods=['POST'])
def print_hello_table():
    # Get form data
    server_addr = request.form['connection_string']
    db_name = request.form['database_name']
    user = request.form['user']
    password = request.form['password']

    # Fetch the hello table
    with create_connection(server_addr, db_name, user, password) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Hello;")
        messages = list(cursor)

    return render_template_string("""
        <h1>Hello Table</h1>
        {% for x in messages %}
        <p>{{ x }}</p>
        {% endfor %}
        """, messages=messages)


def create_connection(server_addr, db_name, user, password):
    connection_string = f"DRIVER={{SQL Server}};SERVER={server_addr};DATABASE={db_name}"
    conn = pyodbc.connect(connection_string, user=user, password=password)
    return conn


if __name__ == '__main__':
    app.run(debug=True)
