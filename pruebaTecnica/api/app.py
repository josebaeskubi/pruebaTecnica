from flask import Flask
import sys

def create_app():
    API_BASE_PATH = '/v1'
    app = Flask(__name__)

    @app.errorhandler(500)
    def code_error(e):
        from traceback import format_tb
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb_list = format_tb(exc_tb)
        return {{'name': str(exc_type.__name__), 'msg': str(exc_value)+"\n"+tb_list[-1]}}, 500
    
    from source.flightRoute.routes import flights_bp
    app.register_blueprint(flights_bp, url_prefix=API_BASE_PATH)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='localhost', port=8000)