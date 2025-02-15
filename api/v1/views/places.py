#!/usr/bin/python3
"""Place objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity
from flask import abort, request, jsonify


@app_views.route(
    "/cities/<city_id>/places", strict_slashes=False, methods=["GET"]
)
def places(city_id):
    """Retrieves the list of Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_list = []
    for place in city.places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route(
    "/places/<place_id>", strict_slashes=False, methods=["GET"]
)
def get_place(place_id):
    """Retrieves a Place object by its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
    "/places/<place_id>", strict_slashes=False, methods=["DELETE"]
)
def place_delete(place_id):
    """Deletes a Place object by ID"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/cities/<city_id>/places", strict_slashes=False, methods=["POST"]
)
def create_place(city_id):
    """Creates a new Place object linked to a given City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, description="Not a JSON")
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)
    if "name" not in data:
        abort(400, description="Missing name")
    new_place = Place(city_id=city.id, **data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route(
    "/places/<place_id>", strict_slashes=False, methods=["PUT"]
)
def update_place(place_id):
    """Updates a Place object by ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, description="Not a JSON")
    place.name = data.get("name", place.name)
    place.description = data.get("description", place.description)
    place.number_rooms = data.get("number_rooms", place.number_rooms)
    place.number_bathrooms = data.get("number_bathrooms",
                                      place.number_bathrooms)
    place.max_guest = data.get("max_guest", place.max_guest)
    place.price_by_night = data.get("price_by_night", place.price_by_night)
    place.latitude = data.get("latitude", place.latitude)
    place.longitude = data.get("longitude", place.longitude)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route(
    "/places_search", methods=["POST"], strict_slashes=False
)
def places_search():
    """
    Retrieves all Place objects based on search criteria provided in JSON body.
    Optional keys:
      - states: list of State ids
      - cities: list of City ids
      - amenities: list of Amenity ids
    """
    req = request.get_json(force=True, silent=True)
    if req is None:
        abort(400, description="Not a JSON")
    states = req.get("states", [])
    cities = req.get("cities", [])
    amenities = req.get("amenities", [])
    if not states and not cities and not amenities:
        all_places = storage.all(Place).values()
        return jsonify([p.to_dict() for p in all_places])
    city_ids = set()
    if states:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in storage.all(City).values():
                    if city.state_id == state_id:
                        city_ids.add(city.id)
    if cities:
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                city_ids.add(city.id)
    if city_ids:
        places_candidates = [
            place for place in storage.all(Place).values()
            if place.city_id in city_ids
        ]
    else:
        places_candidates = list(storage.all(Place).values())
    if amenities:
        amenity_ids = set(amenities)
        filtered_places = []
        for place in places_candidates:
            if hasattr(place, "amenities"):
                place_amen_ids = {amenity.id for amenity in place.amenities}
            else:
                place_amen_ids = set(place.amenity_ids)
            if amenity_ids.issubset(place_amen_ids):
                filtered_places.append(place)
        places_candidates = filtered_places
    return jsonify([place.to_dict() for place in places_candidates])
