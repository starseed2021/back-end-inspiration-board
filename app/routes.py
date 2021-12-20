from flask import Blueprint, request, jsonify, make_response
from app.models.card import Card
from app import db
from app.models.board import Board


boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

# BOARD ROUTES
@boards_bp.route("", methods=["POST", "GET"])
def handle_boards():
    # POST REQUEST
    if request.method == "POST":
        board_request_body = request.get_json()

        new_board = Board(
            owner_name=board_request_body["owner_name"],
            title=board_request_body["title"],
            # card_id=board_request_body["card"]
        )

        db.session.add(new_board)
        db.session.commit()

        new_board_response = new_board.get_board_response()

        return jsonify(new_board_response), 201

    # GET REQUEST
    elif request.method == "GET":
        board_title_query = request.args.get("title")
        board_name_query = request.args.get("owner_name")
        if board_title_query or board_name_query:
            boards = Board.query.filter(Board.title.contains(board_title_query))
            boards = Board.query.filter(Board.owner_name.contains(board_name_query))
        else:
            boards = Board.query.all()

        board_response = [board.get_board_response() for board in boards]

        if board_response == []:
            return jsonify(board_response), 200

        return jsonify(board_response), 200

# GET, PUT, DELETE ONE BOARD AT A TIME
@boards_bp.route("/<board_id>", methods=["GET", "PUT", "DELETE"])
def handle_one_board(board_id):
    if not board_id.isnumeric():
        return jsonify(None), 400

    board = Board.query.get(board_id)

    if board is None: 
        return jsonify({"Message": f"Board {board_id} was not found"}), 404
    
    if request.method == "GET":
        return jsonify(board.get_board_resonse()), 200

    elif request.method == "PUT":
        board_update_request_body = request.get_json()

        if "owner_name" not in board_update_request_body or "title" not in board_update_request_body:
            return jsonify(None), 400

        board.owner_name=board_update_request_body["owner_name"],
        board.title=board_update_request_body["title"],
        # board.card_id=board_update_request_body["card_id"]

        db.session.commit()

        updated_board_response = board.get_board_response()

        return jsonify(updated_board_response), 200
    
    elif request.method == "DELETE":

        db.session.delete(board)
        db.session.commit()

        board_delete_response = board.get_board_response()

        return jsonify(board_delete_response), 200

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
