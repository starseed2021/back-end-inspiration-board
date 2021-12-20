from flask import Blueprint, request, jsonify
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
            card_id=board_request_body["card"]
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
        board.card_id=board_update_request_body["card_id"]

        db.session.commit()

        updated_board_response = board.get_board_response()

        return jsonify(updated_board_response), 200
    
    elif request.method == "DELETE":

        db.session.delete(board)
        db.session.commit()

        board_delete_response = board.get_board_response()

        return jsonify(board_delete_response), 200

