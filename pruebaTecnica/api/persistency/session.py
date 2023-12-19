from sqlalchemy.exc import SQLAlchemyError
from extensions import Session

def dbcommit(func):
    def inner(*args, **kwargs):
        session = Session()  
        try:
            value = func(*args, **kwargs) 
            session.commit()
            return value
        except SQLAlchemyError as e:
            session.rollback()
            return {'error': e.orig}, False
        finally:
            Session.remove()
    return inner