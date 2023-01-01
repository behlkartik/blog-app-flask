from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
if os.environ.get("ENV") == "production":
    app.config.from_object("app.config.ProdConfig")
else:
    app.config.from_object("app.config.ProdConfig")
db = SQLAlchemy(app=app)
migrate = Migrate(app=app, db=db)


from app import routes
