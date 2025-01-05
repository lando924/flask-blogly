from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    with app.app_context():
        db.app = app
        db.init_app(app)
        db.create_all()

"""Models for Blogly."""

class User(db.Model):
    __tablename__= "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                   nullable=False,
                   )
    last_name = db.Column(db.String(30),
                        nullable=True,
                        )
    image_url = db.Column(db.Text(),
                          nullable=True)
    
    def full_name(self):
        """Return full name of user"""
        
        return f"{self.first_name} {self.last_name}"