from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save, pre_delete
from api.models import Mailing, Client, Message
from api.tasks import mailing
from api.celery import app


@receiver(signal=post_save, sender=Mailing)
def schedule_mailing(instance=None, created=False, **kwargs):
    if created:
        mailing_id = instance.id
        filter_params = {}
        if instance.mobile_operator_code:
            filter_params['mobile_operator_code'] = instance.mobile_operator_code
        if instance.tag:
            filter_params['tag'] = instance.tag
        clients = Client.objects.filter(**filter_params).all()
        for client in clients:
            message = Message.objects.create(
                status='SC',
                mailing=instance,
                client=client,
            )
        if instance.ready_to_send:
            instance.task_id = mailing.apply_async((mailing_id,))
            instance.save()
        else:
            instance.task_id = mailing.apply_async((mailing_id,), eta=instance.start_datetime)
            instance.save()


@receiver(signal=pre_delete, sender=Mailing)
def cancel_task(instance=None, **kwargs):
    app.control.revoke(instance.task_id, terminate=True)
