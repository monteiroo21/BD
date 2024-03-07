# Aula 1 Project

Simple Flask webapp project backed by SQL Server.

Distributed for learning purposes.

## Dependencies

- Python3.8+ and SQL Server.
- Poetry (optional, recommended for dependency management)
- Virtualenv (recommended for environment isolation)
- Libraries
  - [Flask](https://flask.palletsprojects.com)
  - Pyodbc
  - [htmx](https://htmx.org) (included in index.html)

Dependencies can be managed using [Poetry](https://python-poetry.org/). 
To install Poetry, follow the [installation guide](https://python-poetry.org/docs/#installation),
then install the project dependencies with: `poetry install`.

Alternatively, you can use pip to install the dependencies from the `requirements.txt` file:
```bash
pipx install -r requirements.txt
```

For a more controlled environment, it's advisable to utilize a virtual environment 
([instal](https://virtualenv.pypa.io/en/latest/installation.html)
, [usage](https://virtualenv.pypa.io/en/latest/user_guide.html)).

## Running

To run the application, use the following command:
```bash
flask run --debug
```

## Recommended resources







