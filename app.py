from flask import Flask
from flask_cors import CORS
from app_container.controllers.metric import metric_controller
import os
app = Flask(__name__)
CORS(app)


app.register_blueprint(metric_controller, url_prefix='/')


if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=3000)
