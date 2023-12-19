def ini_db_session(db):
    from .persistency.models import Base_flights, Routes, Airports, Aircrafts, Airlines, RouteWaypoints, Waypoints
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, scoped_session

    engine_flights = create_engine(db)

    Base_flights.metadata.create_all(bind=engine_flights)

    session_factory = sessionmaker(autocommit=False, autoflush=False)
    session_factory.configure(binds={Routes: engine_flights,
                             Airports: engine_flights,
                             Aircrafts: engine_flights,
                             Airlines: engine_flights,
                             RouteWaypoints: engine_flights,
                             Waypoints: engine_flights})
    session = scoped_session(session_factory)

    Base_flights.query = session.query_property()
    
    return session

Session = ini_db_session("mysql:///flights")