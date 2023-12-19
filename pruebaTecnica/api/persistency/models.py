from sqlalchemy import String, Integer, Column, UniqueConstraint, CheckConstraint, ForeignKey, DateTime, Float, func
from sqlalchemy.orm import declarative_base, relationship, backref

Base_flights = declarative_base()

class Airports(Base_flights):

    __tablename__ = 'Airports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    info = Column(String, nullable=False)

    @staticmethod
    def getAirportbyID(id):
        return Airports.query.get(id)
    
    @staticmethod
    def getAirportByName(airport):
        return Airports.query.filter_by(name = airport).one()

class Aircrafts(Base_flights):

    __tablename__ = 'Aircrafts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    info = Column(String, nullable=False)

    @staticmethod
    def getAircraftbyID(id):
        return Aircrafts.query.get(id)
    
    @staticmethod
    def getAircraftByName(aircraft):
        return Aircrafts.query.filter_by(name = aircraft).one()

class Airlines(Base_flights):

    __tablename__ = 'Airlines'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    info = Column(String, nullable=False)

    @staticmethod
    def getAirlinebyID(id):
        return Airlines.query.get(id)
    
    @staticmethod
    def getAirlineByName(airline):
        return Airlines.query.filter_by(name = airline).one()

class Waypoints(Base_flights):

    __tablename__ = 'Waypoints'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    @staticmethod
    def getWaypointbyID(id):
        return Waypoints.query.get(id)
    
    @staticmethod
    def getWaypointByName(waypoint):
        return Waypoints.query.filter_by(name = waypoint).one()

class Routes(Base_flights):

    __tablename__ = 'Routes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    star = Column(String, nullable=False)
    cruiseLevel = Column(Integer, nullable=False)
    cruiseMach = Column(Float, nullable=False)
    tow = Column(Integer, nullable=False)
    deltaIsa = Column(Float, nullable=False)
    tripFuel = Column(Integer, nullable=False)
    tripDistance = Column(Integer, nullable=False)
    fpl = Column(String, nullable=False)
    depAirportID = Column(Integer, ForeignKey('Airports.id', ondelete="CASCADE"))
    depAirports = relationship("Airports", backref=backref("Routes", cascade="all,delete"))
    arrAirportID = Column(Integer, ForeignKey('Airports.id', ondelete="CASCADE"))
    arrAirports = relationship("Airports", backref=backref("Routes", cascade="all,delete"))
    date = Column(DateTime, nullable=False)
    aircraftID = Column(Integer, ForeignKey('Aircrafts.id', ondelete="CASCADE"))
    aircrafts = relationship("Aircrafts", backref=backref("Routes", cascade="all,delete"))
    airlineID = Column(Integer, ForeignKey('Airlines.id', ondelete="CASCADE"))
    airlines = relationship("Airlines", backref=backref("Routes", cascade="all,delete"))

    def convertToDict(self):
        d = {}
        d['id'] = self.id
        d['name'] = self.name
        d['star'] = self.star
        d['cruiseLevel'] = self.cruiseLevel
        d['cruiseMach'] = self.cruiseMach
        d['tow'] = self.tow
        d['deltaIsa'] = self.deltaIsa
        d['tripFuel'] = self.tripFuel
        d['tripDistance'] = self.tripDistance
        d['fpl'] = self.fpl
        d['departure'] = Airports.getAirportbyID(self.depAirportID).name
        d['arrival'] = Airports.getAirportbyID(self.arrAirportID).name
        d['date'] = self.date
        d['airline'] = Airlines.getAirlinebyID(self.airlineID).name
        d['aircraft'] = Aircrafts.getAircraftbyID(self.aircraftID).name
        d['waypoints'] = []
        for routeWay in RouteWaypoints.getInfoByRoute(self):
            d['waypoints'].append(routeWay.convertToDict())
        return d
    
    @staticmethod
    def getRouteByID(id):
        return Routes.query.get(id)
    
    @staticmethod
    def getRoutesByDepArr(departure, arrival):
        return Routes.query.filter_by(depAirports = departure).filter_by(arrAirports = arrival).all()
    
    @staticmethod
    def getRoutesByDepArrAircraft(departure, arrival, aircraft):
        return Routes.query.filter_by(depAirports = departure).filter_by(arrAirports = arrival).filter_by(aircrafts = aircraft).all()
    
    @staticmethod
    def getRoutesByDepArrAirline(departure, arrival, airline):
        return Routes.query.filter_by(depAirports = departure).filter_by(arrAirports = arrival).filter_by(airlines = airline).all()

    @staticmethod
    def getRouteByFuel(fuel):
        return Routes.query.filter_by(tripFuel = fuel).one()

    @staticmethod
    def getRouteByTime(time):
        return Routes.query.filter_by(time = time).one()

    @staticmethod
    def getRouteByDistance(distance):
        return Routes.query.filter_by(tripDistance = distance).one()

class RouteWaypoints(Base_flights):

    __tablename__ = 'RouteWaypoints'

    routePointID = Column(Integer, primary_key=True, autoincrement=True)
    routeID = Column(Integer, ForeignKey('Routes.id', ondelete="CASCADE"))
    routes = relationship("Routes", backref=backref("RouteWaypoints", cascade="all,delete"))
    waypointID = Column(Integer, ForeignKey('Waypoints.id', ondelete="CASCADE"))
    waypoints = relationship("Waypoints", backref=backref("RouteWaypoints", cascade="all,delete"))
    eet1 = Column(Integer, nullable=False)
    eet2 = Column(Integer, nullable=False)
    eet3 = Column(Integer, nullable=False)
    eet4 = Column(Integer, nullable=False)
    flightLevel = Column(Integer, nullable=True)
    track = Column(Integer, nullable=False)
    windDir = Column(Integer, nullable=False)
    windSpeed = Column(Integer, nullable=False)
    oat = Column(Integer, nullable=True)
    mach = Column(Float, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    def convertToDict(self):
        d = {}
        d['name'] = Waypoints.getWaypointbyID(self.waypointID).name
        d['eet1'] = self.eet1
        d['eet2'] = self.eet2
        d['eet3'] = self.eet3
        d['eet4'] = self.eet4
        d['flightLevel'] = self.flightLevel
        d['track'] = self.track
        d['windDir'] = self.windDir
        d['windSpeed'] = self.windSpeed
        d['oat'] = self.oat
        d['mach'] = self.mach
        d['latitude'] = self.latitude
        d['longitude'] = self.longitude
        return d

    @staticmethod
    def getInfoByRoute(route):
        return RouteWaypoints.query.filter_by(routes = route).all()