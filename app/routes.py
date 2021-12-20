from flask import Blueprint, request, jsonify, make_response
from app.models.card import Card
from app import db

# example_bp = Blueprint('example_bp', __name__)
# Note: the url_prefix should maybe be removed later, but I'll keep it for now 
# for the sake of being able to test with Postman. 
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# --- Card routes --- # 

# Get all cards 
# Note: I think don't think we'll actually need this b/c what we'll have instead 
# is a route that'll allow us to get all cards BY BOARD. 
# i.e. GET - /boards/<board_id>/cards
@cards_bp.route("", methods=["GET"])
def cards():
    cards = Card.query.all()
    cards_response = [card.to_json() for card in cards]
    return jsonify(cards_response), 200

# Add a card 
# Note: Again, I think this should actually be a route undder board since we'd 
# only had a card to a PARTICULAR BOARD. 
# i.e. POST - /boards/<board_id>/cards
@cards_bp.route("", methods=["POST"])
def add_card():
    request_data = request.get_json()
    card = Card(
        message = request_data['message'],
        likes_count = 0
    )
    db.session.add(card)
    db.session.commit()

    return jsonify(card.to_json()), 201

# Update a card's likes_count 
# ######## FINISH THIS ONE ######### 
# @cards_bp.route("/<card_id>/add_like", methods=["PUT"])
# def increment_card_likes_count(card_id):
#     card = Card.query.get(card_id)

#     # add one to the count for this card
#     # do here 

#     # commit it to DB 
#     db.session.commit()

    return jsonify(card.to_json()),200

# Delete a card 
@cards_bp.route("/<card_id>", methods=["DELETE"])
def increment_card_likes_count(card_id):
    card = Card.query.get(card_id)

    db.session.delete(card)
    db.session.commit()

    return f"Card {card_id} has been deleted.", 200