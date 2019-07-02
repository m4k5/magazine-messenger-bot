from django.db import models


# Create your models here.
class Subscriber(models.Model):
    id = models.CharField()
    name = models.CharField()
    # profile_pic = models.ImageField()
    is_subscribed = models.BooleanField(default=True)
    subscribed_from = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id


class MagazineIssue(models.Model):
    title = models.CharField()
