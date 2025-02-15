#!/usr/bin/python3
"""Place - Amenity view module: handles linking and unlinking Amenity objects for a Place"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.amenity import Amenity

@app_views.route("/places/<place_id>/amenities", methods=["GET"], strict_slashes=False)
def get_place_amenities(place_id):
    """
    Retrieves the list of all Amenity objects of a Place.
    If the place_id is not linked to any Place object, raise a 404 error.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenities_list = []
    # For DBStorage, place.amenities is a relationship.
    if hasattr(place, "amenities"):
        for amenity in place.amenities:
            amenities_list.append(amenity.to_dict())
    else:
        # For FileStorage, the Place object has a list attribute amenity_ids.
        for amenity_id in place.amenity_ids:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)

@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes an Amenity object from a Place.
    If the place_id or amenity_id is not linked to any object, or the Amenity is not linked to the Place, raise a 404 error.
    Returns an empty dictionary with status code 200.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    # Check if amenity is linked to the place.
    if hasattr(place, "amenities"):
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
    place.save()
    return jsonify({}), 200

@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """
    Link an Amenity object to a Place.
    No HTTP body is needed.
    If the place_id or amenity_id is not linked to any object, raise a 404 error.
    If the Amenity is already linked to the Place, return the Amenity with status code 200.
    Otherwise, link the Amenity and return it with status code 201.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    # For DBStorage: check if amenity is already linked via the relationship.
    if hasattr(place, "amenities"):
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        # For FileStorage: check if amenity_id is already in the amenity_ids list.
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
    place.save()
    return jsonify(amenity.to_dict()), 201
