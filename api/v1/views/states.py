#!/usr/bin/python3
""" View for State objects that handles all default RESTFul API actions"""


from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """func that retrieves the list of all State objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state_by_id(state_id):
    """func that retrieves a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """func that deletes a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """func that creates a State object"""
    json_data = request.get_json()
    if not json_data:
        abort(400, "Not a JSON")
    if "name" not in json_data:
        abort(400, "Missing name")
    state = State(**json_data)
    storage.new(state)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """func that updates a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        abort(400, "Not a JSON")
    for key, value in json_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
