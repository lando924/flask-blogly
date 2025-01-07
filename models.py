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

    def __repr__(self):
        """Show user id, first and last name"""
        return f"id{self.id} first:{self.first_name} last:{self.last_name}"

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
                          nullable=True,
                          default='https://images.unsplash.com/photo-1735596717044-94c05d6c49dc?q=80&w=2832&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')
   

    def full_name(self):
        """Return full name of user"""
        
        return f"{self.first_name} {self.last_name}"