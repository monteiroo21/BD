from flask import Flask, make_response, render_template, render_template_string, request

from bd_project import music
from bd_project import composer
from bd_project.music import Music
from bd_project.composer import Composer

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
    

if __name__ == "__main__":
    app.run(debug=True)
