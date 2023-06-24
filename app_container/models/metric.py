from app_container.services.metric_services import MetricService


class Metric:
    def __init__(self):
        self.metricService = MetricService()

    def recurring_revenue(self, metric):
        return self.metricService.recurringRevenue(metric)

    def lifetime_value(self, metric):
        return self.metricService.lifetimeValue(metric)
