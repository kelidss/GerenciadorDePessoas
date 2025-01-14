from . import db

class Person(db.Model):
    """Classe de modelo de pessoas."""
    
    __tablename__ = "person"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    
    child = db.relationship('Child', backref='parent', lazy=True)
