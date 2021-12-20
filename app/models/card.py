from app import db

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)

    def to_json(self):
        return {
            "id" : self.id,
            "message" : self.message,
            "likes_count" : self.likes_count,
        }