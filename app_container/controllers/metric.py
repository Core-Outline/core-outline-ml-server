from flask import Blueprint, request, jsonify
from app_container.models.metric import Metric

metric_controller = Blueprint('metric', __name__)
metric = Metric()


@metric_controller.route('/recurring-revenue', methods=['POST'])
def get_recurring_revenue():
    req = request.get_json()
    return jsonify((metric.recurring_revenue(req)))


@metric_controller.route('/recurring-revenue', methods=['POST'])
def get_ltv():
    req = request.get_json()
    return jsonify((metric.lifetime_value(req)))
