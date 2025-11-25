import os
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from . import admin
from app.extensions import db
from app.models import Photo

UPLOAD_FOLDER = "app/static/uploads/"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@admin.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("file")
        title = request.form.get("title")
        description = request.form.get("description")
        tags = request.form.get("tags")

        if not file or file.filename == "":
            flash("No file selected")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Invalid file type")
            return redirect(request.url)

        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Insert DB record
        photo = Photo(
            filename=filename,
            title=title,
            description=description,
            tags=tags
        )
        db.session.add(photo)
        db.session.commit()

        flash("Photo uploaded successfully!")
        return redirect(url_for("admin.upload"))

    return render_template("upload.html")
