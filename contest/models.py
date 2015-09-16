from django.db import models
from django.conf import settings

# Create your models here.
class Administrator(models.Model):
    username = models.CharField(max_length=50, null=False)
    first_name = models.CharField(max_length=512, null=False)
    last_name = models.CharField(max_length=512, null=False)
    email = models.CharField(max_length=512, null=False)
    password = models.CharField(max_length=512)
    enable = models.BooleanField(null=False, default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)


class Contest(models.Model):
    name = models.CharField(max_length=256, null=False)
    image = models.CharField(max_length=512)
    url = models.CharField(max_length=512, null=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_date = models.DateTimeField()
    enable = models.BooleanField(null=False, default=True)
    prize = models.CharField(max_length=512, null=False)
    owner = models.ForeignKey(Administrator, null=False)
    detail = models.CharField(max_length=512)


class Competitor(models.Model):
    first_name = models.CharField(max_length=256, null=False)
    last_name = models.CharField(max_length=256, null=False)
    email = models.CharField(max_length=256, null=False)


class Video(models.Model):
    contest = models.ForeignKey(Contest, null=False)
    created_date = models.DateTimeField(null=False)
    message = models.CharField(max_length=256, null=False)
    READY = '2'
    IN_PROCESS = '1'
    DISABLED = '0'
    VIDEO_STATUS = (
        (READY, 'Ready'),
        (IN_PROCESS, 'In Process'),
        (DISABLED, 'Disabled')
    )
    status = models.CharField(max_length=1,
                                      choices=VIDEO_STATUS,
                                      default=0)
    path_original = models.CharField(max_length=512)
    path_processed = models.CharField(max_length=512)
    owner = models.ForeignKey(Competitor)


class ProfileImage(models.Model):
    image = models.FileField(upload_to='profile/%Y/%m/%d')



