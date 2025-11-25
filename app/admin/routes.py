import os
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_login import login_required
from app.models import Photo, Tag


from . import admin
from app.extensions import db
from app.models import Photo

UPLOAD_FOLDER = "app/static/uploads/"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@admin.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        file = request.files.get("file")
        title = request.form.get("title")
        description = request.form.get("description")
        tags_raw = request.form.get("tags")  # comma-separated input


        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Create Photo object
        photo = Photo(filename=filename, title=title, description=description)

        # Process tags
        if tags_raw:
            # Split by comma and normalize
            tag_names = [t.strip().lower() for t in tags_raw.split(",") if t.strip()]

            for name in tag_names:
                # Check if tag already exists
                tag = Tag.query.filter_by(name=name).first()

                if not tag:
                    tag = Tag(name=name)
                    db.session.add(tag)  # add new tag to session

                # Link tag to photo
                photo.tags.append(tag)

        # Save photo to database
        db.session.add(photo)
        db.session.commit()

        flash("Photo uploaded successfully!", "success")
        return redirect(url_for("admin.upload"))
    # GET request
    return render_template("upload.html")


@admin.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_photo(id):
    photo = Photo.query.get_or_404(id)

    # Delete file from filesystem
    file_path = os.path.join(UPLOAD_FOLDER, photo.filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    # Delete DB entry
    db.session.delete(photo)
    db.session.commit()

    flash("Photo deleted successfully!", "success")
    return redirect(url_for("main.gallery"))

