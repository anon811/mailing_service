from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone


class Mailing(models.Model):
    start_datetime = models.DateTimeField(verbose_name='Начало рассылки')
    stop_datetime = models.DateTimeField(verbose_name='Окончание рассылки')
    text = models.TextField(verbose_name='Текст сообщения')
    mobile_operator_code = models.CharField(max_length=3, blank=True, verbose_name='Код оператора связи')
    tag = models.CharField(max_length=20, blank=True, verbose_name='Тэг')
    task_id = models.CharField(max_length=200, null=True, blank=True)

    @property
    def messages_sent(self):
        return len(self.messages.filter(status='OK'))

    @property
    def messages_scheduled(self):
        return len(self.messages.filter(status='SC'))

    @property
    def messages_error(self):
        return len(self.messages.filter(status='ER'))

    @property
    def message_failed(self):
        return len(self.messages.filter(status='FA'))


    @property
    def ready_to_send(self):
        if self.start_datetime <= timezone.now() <= self.stop_datetime:
            return True
        else:
            return False

    def __str__(self):
        return f'Рассылка {self.id} от {self.start_datetime}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Client(models.Model):
    phone_validator = RegexValidator(regex=r'^7\w{10}$',
                                     message='Введите номер телефона в формате 7XXXXXXXXXX(X - цифра от 0 до 9)')

    phone_number = models.CharField(max_length=11, validators=[phone_validator])
    tag = models.CharField(max_length=20, blank=True, verbose_name='Тэг')
    timezone = models.IntegerField(verbose_name='Часовой пояс')
    mobile_operator_code = models.CharField(max_length=3, blank=True, verbose_name='Код оператора связи')

    def __str__(self):
        return f'Клиент {self.id}. Тлф. № {self.phone_number}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    STATUS_CHOICES = [
        ('OK', 'Message sent'),
        ('SC', 'Scheduled'),
        ('ER', 'An error has occurred'),
        ('FA', 'Sending failed'),
    ]

    dispatch_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Время отправки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Статус отправки')
    mailing = models.ForeignKey(Mailing, related_name='messages', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='message', on_delete=models.CASCADE)

    def __str__(self):
        return f'Сообщение {self.id}, рассылка {self.mailing.text}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
