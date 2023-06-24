from flask import Flask
from app_container.controllers.metric import metric_controller
import os
app = Flask(__name__)


app.register_blueprint(metric_controller, url_prefix='/')


if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=3000)
