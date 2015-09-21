from celery import task
from django.conf import settings
import subprocess
from .models import Video
import datetime
from django.core.mail import send_mail


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
    command=" ffmpeg -i "+settings.MEDIA_ROOT+"/original_videos/"+video_name+" -vcodec libx264 -preset ultrafast -qp 0 -c:a libfdk_aac "+settings.MEDIA_ROOT+"/converted_videos/"+output_name+".mp4"
    subprocess.call(command, shell=True)
    #updates video info
    video.converter_finish_date=datetime.datetime.now()
    video.status=2
    video.path_processed="converted_videos/"+output_name+".mp4"
    video.save()
    send_mail('Your video is ready', 'Hello '+video.owner.first_name+', your video is ready to view. Thanks for play!', settings.EMAIL_HOST_USER,
    [video.owner.email], fail_silently=False)

