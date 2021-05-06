import os
import json
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions
from flask_cors import CORS, cross_origin
from functools import wraps
from waitress import serve
from db_interface import DB_Interface
from flask import (
    jsonify, 
    Response, 
    request, 
    has_request_context, 
    make_response, 
    Flask, 
    abort
)
from dotenv import load_dotenv
from os.path import join, dirname
load_dotenv(join(dirname(__file__), '.env'))


''' Controllers ''' 
from controllers import enumerations_controller
EnumerationsController = enumerations_controller.EnumerationsController


# ''' Data Models ''' 
# from models import Property




''' SERVER INITIALIZATION AND CONFIG '''

app = DB_Interface.get_app_with_db_configured()
@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code

for ex in default_exceptions:
    app.register_error_handler(ex, handle_error)


# API authentication route decorator
def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.args.get('key') and request.args.get('key') == os.environ['API_KEY']:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function

        
CORS(app, support_credentials=True)
# parser = reqparse.RequestParser()
# parser.add_argument('task')

db = SQLAlchemy(app)

''' END SERVER INITIALIZATION AND CONFIG '''



''' ROUTES '''
@app.route("/")
@cross_origin(supports_credentials=True)
@require_appkey
def welcome_text():
    return "This is an authenticated server :)"


@app.route("/api/adjacent_nodes", methods=["GET"])
@cross_origin(supports_credentials=True)
# @require_appkey
def get_adjacent_nodes():

    # res = Property.query.all()
    # print(res)

    return "DSFSDfsdfd"

@app.route("/api/enumerations", methods=["GET"])
@cross_origin(supports_credentials=True)
@require_appkey
def get_enumations():

    data = EnumerationsController.get_all()
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return data

''' END ROUTES '''




''' START UP SERVER '''
if __name__ == '__main__':
    if os.environ['PRODUCTION'] and os.environ['PRODUCTION'] == "True":
        print("Started production server .... :)")
        serve(app, host="0.0.0.0", port=5000) # run production server
    else: 
        app.run(debug=True)   # run default flask server 

''' END START UP SERVER '''