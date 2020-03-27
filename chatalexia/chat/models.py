from django.db import models

from chatalexia.users.models import User


class Message(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Msg sent from")
    text = models.CharField('Message text', max_length=255)


class Room(models.Model):
    messages = models.ManyToManyField(Message, verbose_name="Messages")
    name = models.CharField('Room name', max_length=50)
    admins = models.ManyToManyField(User, verbose_name="Room owners")
    public = models.BooleanField('Room visibility', default=True)

