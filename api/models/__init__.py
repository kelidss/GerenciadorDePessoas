from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .person import Person
from .child import Child