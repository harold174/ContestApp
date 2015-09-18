from celery import task
from django.conf import settings
import subprocess
from .models import Video
import datetime


@task()
def add(x, y):
    return x + y


@task()
def convertVideos(video_name, id):
    output_name = video_name.split(".")
    output_name = output_name[0]
    video = Video.objects.get(pk=id)
    video.converter_start_date=datetime.datetime.now()
    video.save()
    command=" ffmpeg -i "+settings.MEDIA_ROOT+"/original_videos/"+video_name+" "+settings.MEDIA_ROOT+"/converted_videos/"+output_name+".mp4"
    subprocess.call(command, shell=True)
    #updates video info
    video.converter_finish_date=datetime.datetime.now()
    video.status=2
    video.path_processed="converted_videos/"+output_name+".mp4"
    video.save()

