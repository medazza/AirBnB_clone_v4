#!/usr/bin/python3
"""View for City objects that handles all default RESTFul API actions"""


from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_cities(state_id):
    """func that retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """func that retrieves a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """func that deletes a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """func that creates a City object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in json_data:
        return jsonify({"error": "Missing name"}), 400
    json_data["state_id"] = state_id
    city = City(**json_data)
    storage.new(city)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """func that updates a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in json_data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
