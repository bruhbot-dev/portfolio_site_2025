from .extensions import db

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    tags = db.Column(db.String(255))  # comma-separated tags

    def __repr__(self):
        return f"<Photo {self.filename}>"
