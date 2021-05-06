import os
from flask import Flask

class DB_Interface:

    @staticmethod
    def get_app_with_db_configured():
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']
        app.config['BUNDLE_ERRORS'] = os.environ['BUNDLE_ERRORS']

        return app