from . import main
from flask import render_template, request, redirect, url_for, flash
from flask import abort
from app.models import Photo, Tag
from sqlalchemy import or_


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


@main.route("/filter", methods=["GET", "POST"])
def filter_gallery():
    # Load all tags for checkbox list
    all_tags = Tag.query.order_by(Tag.name).all()

    if request.method == "POST":
        selected_tag_ids = request.form.getlist("tags")  # list of tag IDs as strings

        if not selected_tag_ids:
            flash("No tags selected.", "warning")
            return render_template("filter_gallery.html", tags=all_tags, photos=[])

        # Convert IDs to integers
        selected_tag_ids = [int(t) for t in selected_tag_ids]

        # OR logic: photos that have ANY of the selected tags
        photos = (
            Photo.query.join(Photo.tags)
            .filter(Tag.id.in_(selected_tag_ids))
            .all()
        )

        return render_template("filter_gallery.html", tags=all_tags, photos=photos, selected=selected_tag_ids)

    # GET request → show form only
    return render_template("filter_gallery.html", tags=all_tags, photos=None)
