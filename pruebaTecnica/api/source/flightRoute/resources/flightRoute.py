from flask.views import MethodView
from flask import request
import json
from source.flightRoute.logic.funcs import create_route, get_flights, get_efficient_flights, get_proposed_flight

class FlightRoute(MethodView):

    def get(self):
        departure = request.args.get('departure')
        arrival = request.args.get('arrival')
        if departure is None or arrival is None:
            return {'error': 'Departure and arrival are mandatory'}, 400
        airline = request.args.get('airline')
        aircraft = request.args.get('aircraft')
        response = get_flights(departure, arrival, airline, aircraft)
        return {'routes': response},200
    
    def post(self):
        data = request.json
        msg, succes = create_route(data)
        if succes:
            return msg, 200
        else:
            return msg, 409
        
    
class EfficientFlight(MethodView):

    def get(self):
        departure = request.args.get('departure')
        arrival = request.args.get('arrival')
        if departure is None or arrival is None:
            return {'error': 'Departure and arrival are mandatory'}, 400
        getBy = request.args.get('getBy')
        if getBy is not ['time', 'fuel', 'both']:
            return {'error': 'Not allowed method'}, 400
        response = get_efficient_flights(departure, arrival, getBy)
        return response, 200
    
class ProposedFlight(MethodView):

    def get(self):
        existingRoute = request.args.get('existingRoute')
        data = json.loads(existingRoute)
        response = get_proposed_flight(data)
        return response, 200