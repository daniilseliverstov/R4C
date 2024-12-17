from django.apps import AppConfig


class OrdersConfig(AppConfig):
    name = 'orders'

    def ready(self):
        from robots.signal import check_robot_availability
