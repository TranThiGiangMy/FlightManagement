from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import cloudinary


app = Flask(__name__)
app.secret_key = '$%^*&())(*&%^%4678675446&#%$%^&&*^$&%&*^&^'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/flightmanagement?charset=utf8mb4' % quote('123456789')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

cloudinary.config(cloud_name='dv2y8ynkx',
                  api_key='238948479572549',
                  api_secret='tGIukDd3WlboSNpb-bTYF_MLqTY-A')

db = SQLAlchemy(app=app)