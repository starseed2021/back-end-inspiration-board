from app import db
from sqlalchemy.orm import backref

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_name = db.Column(db.String)
    title = db.Column(db.String)
    card_id = db.Column(db.Integer, db.ForeignKey("card.id"), nullable=False)
    card = db.relationship("Card", backref=backref("cards", cascade="delete"))


    
