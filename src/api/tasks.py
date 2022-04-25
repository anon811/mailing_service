import os
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout
from celery import shared_task
from api.celery import app
from api.models import Mailing, Client, Message

URL = os.environ.get('URL')
TOKEN = os.environ.get('TOKEN')


@shared_task
def mailing(mailing_id):
    mailing_instance = Mailing.objects.get(id=mailing_id)
    for message in mailing_instance.messages.all():
        send_message.apply_async((message.id, URL, TOKEN))


@shared_task
def send_message(message_id, url, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }
    message = Message.objects.get(id=message_id)
    data = {
        'id': message_id,
        'phone': message.client.phone_number,
        'text': message.mailing.text,
    }
    try:
        request_url = url + str(message_id)
        response = requests.post(url=request_url, headers=headers, json=data)
        if response.status_code == 200:
            message.status = 'OK'
            message.save()
        else:
            message.status = 'FA'
            message.save()
    except HTTPError:
        message.status = 'ER'
        message.save()
    except ConnectionError:
        message.status = 'ER'
        message.save()
    except Timeout:
        message.status = 'ER'
        message.save()
