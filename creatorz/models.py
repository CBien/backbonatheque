import requests
import logging
from django.db import models
from django.utils.timezone import now
from django.urls import reverse

logger = logging.getLogger()


class Customer(models.Model):
    firstname = models.TextField()
    lastname = models.TextField()


class MusicianAgent(models.Model):
    name = models.TextField()


class Musician(models.Model):
    firstname = models.TextField()
    lastname = models.TextField()
    birthday = models.DateField()
    nickname = models.TextField()
    band = models.TextField()
    instrument = models.TextField()
    agent = models.ForeignKey(MusicianAgent, null=True, blank=True, on_delete=models.SET_NULL)

    @property
    def age(self, today=None):
        today = today or now()
        return (today - self.birthday).days // 365


class Album(models.Model):
    title = models.TextField()
    description = models.TextField()
    release_date = models.DateField()
    nb_tracks = models.PositiveIntegerField()
    musician = models.ForeignKey(Musician, null=True, blank=True, on_delete=models.SET_NULL, related_name="albums")

    def toggle_playing(self, customer):
        last_event = self.playbacks.filter(customer=customer).order_by("-date_created").first()
        if not last_event or last_event.status == "STOP":
            status = "START"
        else:
            status = "STOP"
        playback = self.playbacks.create(customer=customer, status=status)
        remote_url = "http://localhost:8000" + reverse("major-playback-list")
        try:
            response = requests.post(remote_url, json=playback.serialize(), timeout=1)
            if response.status_code != 201:
                logger.exception("Error occured")
        except Exception as e:
            logger.exception("Timeout occured")


class Playback(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=100, choices=(
        ("START", "Customer starts playing"),
        ("STOP", "Customer stops playing"),
    ))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="playbacks")
    album = models.ForeignKey(Album, on_delete=models.PROTECT, related_name="playbacks")

    def serialize(self):
        return {
            "status": self.status,
            "customer": self.customer_id,
            "album": self.album_id,
        }

class WriterAgent(models.Model):
    name = models.TextField()


class Writer(models.Model):
    firstname = models.TextField()
    lastname = models.TextField()
    publisher = models.TextField()
    agent = models.ForeignKey(WriterAgent, null=True, blank=True, on_delete=models.SET_NULL)


class Book(models.Model):
    title = models.TextField()
    description = models.TextField()
    publication_date = models.DateField()
    writer = models.ForeignKey(Writer, null=True, blank=True, on_delete=models.SET_NULL, related_name="books")
