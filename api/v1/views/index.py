#!/usr/bin/python3
"""Index module"""
from api.v1.views import app_views
from flask import jsonify


def get_status():
    """Returns JSON status"""
    return jsonify({"status": "OK"})
