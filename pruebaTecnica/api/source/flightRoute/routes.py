from flask import Blueprint
from .resources.flightRoute import FlightRoute, EfficientFlight, ProposedFlight

flights_bp = Blueprint('flights', __name__)
flights_bp.add_url_rule('/flight', view_func=FlightRoute.as_view('flights'))
flights_bp.add_url_rule('/flight/efficient', view_func=EfficientFlight.as_view('efficientFlight'))
flights_bp.add_url_rule('/flight/proposed', view_func=ProposedFlight.as_view('proposedFlight'))