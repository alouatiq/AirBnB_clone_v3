#!/usr/bin/python3
"""Initialize Blueprint for views"""
from flask import Blueprint  # Moved import to top
from api.v1.views.cities import *
from api.v1.views.states import *
from api.v1.views.index import *  # Keep wildcard import if required


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Optionally import the routes after app_views is created:
# Import index routes

# Import states routes
# Import cities routes
