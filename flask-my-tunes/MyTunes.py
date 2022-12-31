import sqlite3
from flask import g, Flask, render_template, template_rendered, request, redirect

app = Flask(__name__)

#Data base
DATABASE = "chinook.db"

#opening chinook.db defs

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


#Homepage
@app.route("/")

#Defining Hopepage
def artists_page():
    artists = query_db("Select * From artists")
    return render_template("artists.html",artists = artists)



#Artist Page -- Albums
@app.route("/artist/<artistid>/")
def artist_albums(artistid):
    albums = query_db("SELECT * FROM albums WHERE artistid = " + str(artistid))
    return render_template("albums.html", albums = albums)


#Artist Page -- Tracks
@app.route("/album/<albumid>/", methods = ["GET", "POST"])
def album_tracks(albumid):
    if request.method == "POST":
        name = request.form.get("name")
        composer = request.form.get("composer")
        timems = request.form.get("time")
        genre = request.form.get("genre")
        query = 'INSERT INTO tracks(Name, MediatypeId, AlbumId, GenreId, Composer, Milliseconds, UnitPrice) VALUES ("' + str(name) + ',' + str(1) + ',' + str(albumid) + ',' + str(genre) + ',' + str(composer) + ',' + str(timems) + ',' + str(0.99) + '")'
        newname = query_db(query)
        get_db().commit()
        return redirect("/")
    asongs = query_db("SELECT tracks.Name AS Song, tracks.AlbumId, artists.Name, Title FROM tracks INNER JOIN albums ON tracks.albumid = albums.albumid INNER JOIN artists ON albums.artistid = artists.artistid WHERE albums.albumid = " + str(albumid))
    genres = query_db("SELECT * FROM genres")
    return render_template("tracks.html", asongs = asongs, genres = genres)

#Artist Page -- Track Info
@app.route("/new_artist/", methods = ["GET", "POST"])
def create_artist():
    if request.method == "POST":
        name = request.form.get("name")
        query = 'INSERT INTO artists(Name) VALUES("' + name + '")'
        newname = query_db(query)
        get_db().commit()
        return redirect("/")
    return render_template("artistnew.html")