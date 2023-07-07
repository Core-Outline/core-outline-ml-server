from app_container.services.metric_services import MetricService


class Metric:
    def __init__(self):
        self.metricService = MetricService()

    def recurring_revenue(self, metric):
        return self.metricService.recurringRevenue(metric)

    def lifetime_value(self, metric):
        return self.metricService.lifetimeValue(metric)

    def customer_segmentation(self, metric):
        return self.metricService.customerSegmentation(metric)
    
    def expenses(self, metric):
        return self.metricService.expenses(metric)

    def growth_rate(self, metric):
        return self.metricService.growthRate(metric)
    
    def growth_period(self, metric):
        return self.metricService.growthPeriod(metric)