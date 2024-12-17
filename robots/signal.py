from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from ..orders.models import Order


@receiver(post_save, sender='robots.Robot')
def check_robot_availability(sender, instance, created, **kwargs):
    if not created and instance.is_available:
        # Отправляем письмо клиенту, если робот стал доступен
        subject = 'Робот снова в наличии'
        message = f'''
            Добрый день! 
            Недавно вы интересовались нашим роботом модели {instance.model}, версии {instance.version}. 
            Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.
        '''

        # Здесь нужно получить email клиента из заказа
        order = Order.objects.filter(robot_serial=instance.serial).first()
        if order:
            recipient_email = order.customer.email
            send_mail(
                subject,
                message,
                'noreply@example.com',  # Адрес отправителя
                [recipient_email],
                fail_silently=False,
            )