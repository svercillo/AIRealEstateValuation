from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Property(db.Model):
    __tablename__ = 'property'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    address = db.Column(db.String(255))
    sold_price = db.Column(db.Float)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    rooms = db.Column(db.Integer)
    soldOn = db.Column(db.DateTime)
    soldDate = db.Column(db.DateTime)
    listedOn = db.Column(db.DateTime)
    longitude = db.Column(db.Numeric(9,6))
    latitude = db.Column(db.Numeric(9,6))
    style = db.Column(db.String(255))
    area = db.Column(db.Integer)
    parking = db.Column(db.Integer)
    kitchens = db.Column(db.Integer)
    district = db.Column(db.String(255))
    amenities = db.Column(db.JSON)


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()