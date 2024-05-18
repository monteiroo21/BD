from flask import Flask, make_response, render_template, render_template_string, request

from bd_project import music
from bd_project.music import Music

app = Flask(__name__)


@app.route("/")
def base():
    musics = music.list_all()
    return render_template("index.html", musics=musics)


@app.route("/music-list", methods=["GET"])
def music_list():
    musics = music.list_all()
    return render_template("music_list.html", musics=musics)
    

if __name__ == "__main__":
    app.run(debug=True)
