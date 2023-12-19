from extensions import Session
from api.persistency.models import Routes, Airports, Aircrafts, Airlines, RouteWaypoints, Waypoints
from api.persistency.session import dbcommit

@dbcommit
def create_route(data):
    session = Session()
    airline = Airlines.getAirlineByName(data['airline'])
    aircraft = Aircrafts.getAircraftByName(data['aircraft'])
    departure = Airports.getAirportByName(data['departure'])
    arrival = Airports.getAirportByName(data['arrival'])
    route = Routes(name = data['route']['name'], star = data['route']['star'], cruiseLevel = data['route']['cruiseLevel']
                , cruiseMach = data['route']['cruiseMach'], tow = data['route']['tow'], deltaIsa = data['route']['deltaIsa']
                , tripFuel = data['route']['tripFuel'], tripDistance = data['route']['tripDistance'], fpl = data['route']['tripDistance']
                , date = data['date'])
    route.depAirports = departure
    route.arrAirports = arrival
    route.aircrafts = aircraft
    route.airlines = airline
    session.add(route)
    session.flush()
    for waypoint in data['route']['waypoints']:
        try: 
            flightLevel = waypoint['flightLevel']
        except KeyError: 
            flightLevel = None
        try: 
            oat = waypoint['oat']
        except KeyError: 
            oat = None
        try: 
            mach = waypoint['mach']
        except KeyError: 
            mach = None
        wayp = Waypoints.getWaypointByName(waypoint['name'])
        waypointRoute = RouteWaypoints(eet1 = waypoint['ett'][0], eet2 = waypoint['ett'][1], eet3 = waypoint['ett'][2], eet4 = waypoint['ett'][3]
                                    , flightLevel = flightLevel, track = waypoint['track'], winDir = waypoint['winDir'], winSpeed = waypoint['winSpeed']
                                    , oat = oat, mach = mach, latitude = waypoint['latitude'], longitude = waypoint['longitude'])
        waypointRoute.waypoints = wayp
        waypointRoute.routes = route
        session.add(waypointRoute)
        session.flush()
    return {}, True

def get_flights(departure, arrival, airline, aircraft):
    response = []
    if airline is None and aircraft is None:
        routes = Routes.getRoutesByDepArr(Airports.getAirportByName(departure), Airports.getAirportByName(arrival))
        for route in routes:
            response.append(route.convertToDict())
    elif airline is not None and aircraft is None:
        routes = Routes.getRoutesByDepArrAirline(Airports.getAirportByName(departure), Airports.getAirportByName(arrival), Airlines.getAirlineByName(airline))
        for route in routes:
            response.append(route.convertToDict())
    else:
        routes = Routes.getRoutesByDepArrAircraft(Airports.getAirportByName(departure), Airports.getAirportByName(arrival), Aircrafts.getAircraftByName(aircraft))
        for route in routes:
            response.append(route.convertToDict())
    return response

def get_efficient_flights(departure, arrival, getBy):
    session = Session()
    if getBy is 'fuel':
        sql_sentence = f'SELECT MIN(tripFuel) FROM Route WHERE depAirportID = {Airports.getAirportByName(departure).id} AND arrAirportID = {Airports.getAirportByName(arrival).id}'
        result = session.execute(sql_sentence)
        for elem in result: 
            min_value = elem[0]
        route = Routes.getRouteByFuel(min_value) 
    elif getBy is 'time':
        #Desconozco si alguno de los campos se refiere al tiempo o es necesario calcularlo con la distancia y el mach a la hora de almacenar la información
        sql_sentence = f'SELECT MIN(time) FROM Route WHERE depAirportID = {Airports.getAirportByName(departure).id} AND arrAirportID = {Airports.getAirportByName(arrival).id}'
        result = session.execute(sql_sentence)
        for elem in result: 
            min_value = elem[0]
        route = Routes.getRouteByTime(min_value) 
    else:
        sql_sentence = f'SELECT id, tripFuel+time FROM Route WHERE depAirportID = {Airports.getAirportByName(departure).id} AND arrAirportID = {Airports.getAirportByName(arrival).id}'
        result = session.execute(sql_sentence)
        min_elem = result[0][1]
        for elem in result:
            if elem[1] < min_elem:
                routeID = elem[0]
                min_elem = elem[1]
        route = Routes.getRouteByID(routeID)
    Session.remove()
    return route.convertToDict()

def get_proposed_flight(data):
    session = Session()
    sql_sentence = f"SELECT MIN(tripDistance) FROM Route WHERE depAirportID = {Airports.getAirportByName(data['departure']).id} AND arrAirportID = {Airports.getAirportByName(data['arrival']).id}"
    result = session.execute(sql_sentence)
    for elem in result: 
        min_value = elem[0]
    route = Routes.getRouteByDistance(min_value)
    Session.remove()
    return route.convertToDict()