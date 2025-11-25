from . import main
from flask import render_template
from flask import abort
from app.models import Photo


@main.route("/")
def home():
    print("Home route hit!")   # DEBUG LINE
    return render_template("home.html")


@main.route("/gallery")
def gallery():
    photos = Photo.query.all()
    return render_template("gallery.html", photos=photos)


@main.route("/photo/<int:id>")
def photo_detail(id):
    photo = Photo.query.get_or_404(id)
    return render_template("photo_detail.html", photo=photo)